"""T-learner uplift model, Qini evaluation and a targeting rule that cuts spend while holding conversions."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir, output_dir  # noqa: E402

FEATS = ["recency_days", "frequency_12m", "monetary_12m", "email_engagement", "discount_user"]
ANNUAL_SPEND = 2_000_000


def qini_auc(y, t, uplift):
    order = np.argsort(-uplift)
    y, t = y[order], t[order]
    ct, cc = np.cumsum(t), np.cumsum(1 - t)
    yt, yc = np.cumsum(y * t), np.cumsum(y * (1 - t))
    q = yt - yc * np.divide(ct, cc, out=np.zeros_like(ct, dtype=float), where=cc > 0)
    rand = np.linspace(0, q[-1], len(q))
    return (q - rand).mean(), q


def main():
    df = pd.read_csv(data_dir(__file__) / "campaign.csv")
    tr, te = train_test_split(df, test_size=0.5, random_state=0, stratify=df.treatment)
    mk = lambda: HistGradientBoostingClassifier(max_iter=200, learning_rate=0.05, max_depth=3, random_state=0)
    m1 = mk().fit(tr[tr.treatment == 1][FEATS], tr[tr.treatment == 1].converted)
    m0 = mk().fit(tr[tr.treatment == 0][FEATS], tr[tr.treatment == 0].converted)
    te = te.copy()
    te["p1"], te["p0"] = m1.predict_proba(te[FEATS])[:, 1], m0.predict_proba(te[FEATS])[:, 1]
    te["uplift"] = te.p1 - te.p0

    q_model, _ = qini_auc(te.converted.values, te.treatment.values, te.uplift.values)
    print(f"Qini (area above random), model: {q_model:.1f}  — positive = better than random targeting")

    # Segments
    hi_base = te.p0 >= te.p0.quantile(0.7)
    te["segment"] = np.select([te.uplift < -0.002, te.uplift >= te.uplift.quantile(0.5), hi_base],
                              ["Do-not-disturb", "Persuadable", "Sure thing"], "Lost cause")
    seg = te.groupby("segment").apply(lambda g: pd.Series({
        "share": len(g) / len(te),
        "observed_lift_pts": 100 * (g[g.treatment == 1].converted.mean() - g[g.treatment == 0].converted.mean())}))
    print("\nSegments (observed lift on held-out data)")
    print(seg.round(3).to_string())

    # Targeting: send to top-k% by predicted uplift; incremental conversions estimated on held-out randomised data
    tot_inc = te[te.treatment == 1].converted.mean() - te[te.treatment == 0].converted.mean()
    print(f"\nBlanket campaign incremental conversion rate: {tot_inc * 100:.2f} pts per customer")
    base_rate = te[te.treatment == 0].converted.mean()       # conversions that happen without any offer
    total_blanket = base_rate + tot_inc
    print("Target share | total conversions vs blanket campaign")
    best = None
    for share in (1.0, 0.9, 0.8, 0.75, 0.7, 0.6, 0.5):
        cut = te.uplift.quantile(1 - share)
        sel = te[te.uplift >= cut]
        inc = (sel[sel.treatment == 1].converted.mean() - sel[sel.treatment == 0].converted.mean()) * len(sel) / len(te)
        change = (base_rate + inc) / total_blanket - 1
        print(f"   {share:>5.0%}     | {change:+.1%}")
        if change >= -0.02 and (best is None or share < best[0]):
            best = (share, change)
    share, change = best
    print(f"\nRule: contact the top {share:.0%} by predicted uplift → spend −{1 - share:.0%} "
          f"(≈${(1 - share) * ANNUAL_SPEND:,.0f}/yr), total conversions {change:+.1%} (held flat within ±2%)")
    te[["customer_id", "uplift", "segment"]].to_csv(output_dir(__file__) / "uplift_scores.csv", index=False)


if __name__ == "__main__":
    main()
