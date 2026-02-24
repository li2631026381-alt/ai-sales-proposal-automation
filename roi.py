# roi.py
from dataclasses import dataclass

@dataclass
class ROIInput:
    proposals_per_week: int
    hours_before: float
    hours_after: float
    cost_per_hour_hkd: float
    tool_monthly_cost_hkd: float = 0.0  # 你也可以设成某个订阅费

def compute_roi(x: ROIInput) -> dict:
    weekly_hours_saved = max(0.0, (x.hours_before - x.hours_after) * x.proposals_per_week)
    monthly_hours_saved = weekly_hours_saved * 4.0
    monthly_cost_saved = monthly_hours_saved * x.cost_per_hour_hkd
    annual_saving = (monthly_cost_saved - x.tool_monthly_cost_hkd) * 12.0

    net_monthly_benefit = max(0.0, monthly_cost_saved - x.tool_monthly_cost_hkd)
    payback_months = None
    if x.tool_monthly_cost_hkd > 0 and net_monthly_benefit > 0:
        # 如果你把“工具成本”当月成本，就不用回本期；这里给一个示例
        payback_months = 1.0

    return {
        "weekly_hours_saved": round(weekly_hours_saved, 2),
        "monthly_hours_saved": round(monthly_hours_saved, 2),
        "monthly_cost_saved_hkd": round(monthly_cost_saved, 0),
        "annual_net_saving_hkd": round(annual_saving, 0),
        "payback_months": payback_months,
    }