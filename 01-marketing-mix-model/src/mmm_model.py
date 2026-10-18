"""
Bayesian Marketing Mix Model and budget optimiser.

1. Geometric adstock + Hill saturation per channel; decay and half-saturation chosen by search on hold-out error.
2. Conjugate Bayesian linear regression (Normal prior, noise variance from OLS residuals) -> posterior draws
   -> channel ROI with 90% credible intervals.
3. SLSQP optimiser re-allocates a fixed total budget, each channel bounded to ±30% of current spend.
"""
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir, output_dir  # noqa: E402

CHANNELS = ["tv", "digital", "print", "radio", "field"]
DECAYS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
HALFS = [0.6, 0.9, 1.2, 1.5, 1.8]
rng = np.random.default_rng(7)


def adstock(x, decay):
    out = np.zeros_like(x, dtype=float)
    for t in range(len(x)):
        out[t] = x[t] + (decay * out[t - 1] if t else 0)
    return out


def transform(spend, decay, half, scale):
    """Normalised adstock followed by Hill saturation; `scale` is the steady-state adstock of an average week."""
    a = adstock(spend, decay) / scale
    return a / (a + half)


def design(df, params):
    t = np.arange(len(df))
    cols = {"intercept": np.ones(len(df)), "trend": t / 52,
            "sin52": np.sin(2 * np.pi * t / 52), "cos52": np.cos(2 * np.pi * t / 52),
            "price": df["price_index"].values - 1, "promo": df["promo_flag"].values}
    for ch in CHANNELS:
        d, h, s = params[ch]
        cols[ch] = transform(df[f"spend_{ch}"].values, d, h, s)
    return pd.DataFrame(cols)


def bayes_fit(X, y, prior_mean, prior_sd):
    """Conjugate Bayesian linear regression. Returns posterior mean and covariance."""
    beta_ols, *_ = np.linalg.lstsq(X, y, rcond=None)
    sigma2 = np.sum((y - X @ beta_ols) ** 2) / (len(y) - X.shape[1])
    prior_prec = np.diag(1 / prior_sd ** 2)
    post_cov = np.linalg.inv(X.T @ X / sigma2 + prior_prec)
    post_mean = post_cov @ (X.T @ y / sigma2 + prior_prec @ prior_mean)
    return post_mean, post_cov


def priors(columns):
    m, s = np.zeros(len(columns)), np.full(len(columns), 1000.0)
    for i, c in enumerate(columns):
        if c in CHANNELS:  # agreed in workshops: media has a positive effect of plausible size
            m[i], s[i] = 50.0, 60.0
    return m, s


def main():
    df = pd.read_csv(data_dir(__file__) / "mmm_weekly.csv", parse_dates=["week_start"])
    y = df["net_revenue"].values
    train, test = slice(0, 130), slice(130, None)
    means = {ch: df[f"spend_{ch}"].mean() for ch in CHANNELS}

    # 1. adstock / saturation search (coordinate descent on hold-out MAPE)
    params = {ch: (0.3, 1.2, means[ch] / 0.7) for ch in CHANNELS}
    for _ in range(2):
        for ch in CHANNELS:
            best = None
            for d, h in itertools.product(DECAYS, HALFS):
                trial = dict(params, **{ch: (d, h, means[ch] / (1 - d))})
                X = design(df, trial).values
                b, *_ = np.linalg.lstsq(X[train], y[train], rcond=None)
                mape = np.mean(np.abs((y[test] - X[test] @ b) / y[test]))
                if best is None or mape < best[0]:
                    best = (mape, trial[ch])
            params[ch] = best[1]

    # 2. Bayesian fit: hold-out check on train, then final fit on all data
    Xdf = design(df, params)
    pm, ps = priors(Xdf.columns)
    mu_tr, _ = bayes_fit(Xdf.values[train], y[train], pm, ps)
    holdout_mape = np.mean(np.abs((y[test] - Xdf.values[test] @ mu_tr) / y[test]))
    mu, cov = bayes_fit(Xdf.values, y, pm, ps)
    draws = rng.multivariate_normal(mu, cov, size=2000)
    idx = {c: i for i, c in enumerate(Xdf.columns)}

    # 3. contribution and ROI with credible intervals
    rows = []
    for ch in CHANNELS:
        spend = df[f"spend_{ch}"].sum()
        roi = draws[:, idx[ch]] * Xdf[ch].sum() / spend
        rows.append(dict(channel=ch, spend_lakh=round(spend), contribution_lakh=round(mu[idx[ch]] * Xdf[ch].sum()),
                         roi_mean=roi.mean(), roi_p05=np.percentile(roi, 5), roi_p95=np.percentile(roi, 95),
                         decay=params[ch][0], half_sat=params[ch][1]))
    roi_df = pd.DataFrame(rows).sort_values("roi_mean", ascending=False)
    print(f"Hold-out MAPE (last 26 weeks): {holdout_mape:.1%}")
    print("\nChannel ROI (₹ revenue per ₹ spend, 90% credible interval)")
    print(roi_df.round(2).to_string(index=False))
    print(f"\nMarketing ROI (attributed): {roi_df.contribution_lakh.sum() / roi_df.spend_lakh.sum():.2f}x")

    # 4. budget optimiser on steady-state annual response curves
    beta = {ch: mu[idx[ch]] for ch in CHANNELS}

    def annual_media_revenue(weekly):
        total = 0.0
        for ch, s in zip(CHANNELS, weekly):
            d, h, scale = params[ch]
            a = (s / (1 - d)) / scale
            total += 52 * beta[ch] * a / (a + h)
        return total

    current = np.array([means[ch] for ch in CHANNELS])
    res = minimize(lambda w: -annual_media_revenue(w), current, method="SLSQP",
                   bounds=[(0.7 * c, 1.3 * c) for c in current],
                   constraints=[{"type": "eq", "fun": lambda w: w.sum() - current.sum()}])
    opt = res.x
    plan = pd.DataFrame({"channel": CHANNELS, "current_annual_lakh": (current * 52).round(0),
                         "optimal_annual_lakh": (opt * 52).round(0)})
    plan["change_pct"] = ((plan.optimal_annual_lakh / plan.current_annual_lakh - 1) * 100).round(1)
    base, new = annual_media_revenue(current), annual_media_revenue(opt)
    print("\nBudget optimiser (same total, each channel within ±30%)")
    print(plan.to_string(index=False))
    print(f"Share of budget re-allocated: {np.abs(opt - current).sum() / 2 / current.sum():.1%}")
    print(f"Media-driven revenue: {base:,.0f} -> {new:,.0f} lakh/yr (+{new / base - 1:.1%})")

    out = output_dir(__file__)
    roi_df.to_csv(out / "channel_roi.csv", index=False)
    plan.to_csv(out / "optimal_plan.csv", index=False)
    print(f"\nSaved results to {out}")


if __name__ == "__main__":
    main()
