from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AccountSnapshot:
    account_id: str
    account_name: str
    region: str
    segment: str
    contract_value: int
    renewal_window_days: int
    executive_engagement_score: int
    product_adoption_score: int
    support_tickets_90d: int
    open_escalations: int
    payment_delay_days: int
    health_score: int
    churn_risk: float

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["risk_band"] = risk_band(self.churn_risk)
        return payload


def risk_band(probability: float) -> str:
    if probability >= 0.75:
        return "critical"
    if probability >= 0.55:
        return "elevated"
    if probability >= 0.30:
        return "watch"
    return "stable"
