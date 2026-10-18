"""Business value of the real-time CRM program. All unit values are configurable assumptions."""
ASSUMPTIONS = {
    "annual_appointments": 3_300_000,
    "no_show_before": 0.18,
    "no_show_after": 0.138,
    "avg_net_revenue_per_visit_usd": 160,       # assumption — blended outpatient net revenue
    "contact_centre_agents": 400,
    "paid_hours_per_agent_year": 1_880,
    "handle_time_share_of_paid_time": 0.55,     # share of agent time spent handling calls
    "aht_reduction": 0.17,
    "loaded_cost_per_agent_hour_usd": 32,
    "sms_before_per_year": 6_600_000,            # 2 reminders per appointment
    "sms_after_per_year": 4_300_000,             # low-risk get one, high-risk go to agents
    "sms_unit_cost_usd": 0.0125,
}


def main(a=ASSUMPTIONS):
    recovered = a["annual_appointments"] * (a["no_show_before"] - a["no_show_after"])
    visit_rev = recovered * a["avg_net_revenue_per_visit_usd"]
    hours_saved = (a["contact_centre_agents"] * a["paid_hours_per_agent_year"]
                   * a["handle_time_share_of_paid_time"] * a["aht_reduction"])
    agent_value = hours_saved * a["loaded_cost_per_agent_hour_usd"]
    sms_value = (a["sms_before_per_year"] - a["sms_after_per_year"]) * a["sms_unit_cost_usd"]
    print(f"No-show drop: {a['no_show_before']:.1%} -> {a['no_show_after']:.1%} "
          f"({(a['no_show_before'] - a['no_show_after']) * 100:.1f} pts)")
    print(f"Recovered completed visits / yr: {recovered:,.0f}")
    print(f"Revenue from recovered visits:   ${visit_rev:,.0f}")
    print(f"Agent hours freed / yr:          {hours_saved:,.0f}  (${agent_value:,.0f})")
    print(f"SMS cost avoided / yr:           ${sms_value:,.0f}")
    print("Readmission penalty avoidance is reported separately by finance (CMS HRRP).")


if __name__ == "__main__":
    main()
