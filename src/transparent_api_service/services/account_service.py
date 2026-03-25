from __future__ import annotations

import json
from pathlib import Path

from ..models import AccountSnapshot, risk_band


class AccountService:
    def __init__(self, accounts: list[AccountSnapshot]) -> None:
        self._accounts = accounts
        self._account_map = {account.account_id: account for account in accounts}

    @classmethod
    def from_default_data_root(cls) -> "AccountService":
        root = Path(__file__).resolve().parents[3]
        dataset_path = root / "data" / "account_health_snapshot.json"
        payload = json.loads(dataset_path.read_text(encoding="utf-8"))
        accounts = [AccountSnapshot(**item) for item in payload]
        return cls(accounts)

    def summary(self) -> dict[str, object]:
        accounts = self._accounts
        segment_counts: dict[str, int] = {}
        region_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}

        for account in accounts:
            segment_counts[account.segment] = segment_counts.get(account.segment, 0) + 1
            region_counts[account.region] = region_counts.get(account.region, 0) + 1
            band = risk_band(account.churn_risk)
            risk_counts[band] = risk_counts.get(band, 0) + 1

        avg_health = round(sum(account.health_score for account in accounts) / len(accounts), 2)
        avg_risk = round(sum(account.churn_risk for account in accounts) / len(accounts), 4)
        total_contract_value = sum(account.contract_value for account in accounts)

        return {
            "portfolio_size": len(accounts),
            "average_health_score": avg_health,
            "average_churn_risk": avg_risk,
            "total_contract_value": total_contract_value,
            "segment_mix": segment_counts,
            "region_mix": region_counts,
            "risk_band_mix": risk_counts,
        }

    def high_risk_accounts(self, limit: int = 10, region: str | None = None) -> list[dict[str, object]]:
        accounts = self._accounts
        if region:
            accounts = [account for account in accounts if account.region.lower() == region.lower()]
        ranked = sorted(accounts, key=lambda account: (account.churn_risk, -account.contract_value), reverse=True)
        return [account.to_dict() for account in ranked[:limit]]

    def get_account(self, account_id: str) -> dict[str, object] | None:
        account = self._account_map.get(account_id)
        return None if account is None else account.to_dict()

    def recommendations(self, account_id: str) -> dict[str, object] | None:
        account = self._account_map.get(account_id)
        if account is None:
            return None

        actions: list[str] = []
        if account.executive_engagement_score < 45:
            actions.append("Schedule an executive business review within 14 days.")
        if account.support_tickets_90d >= 6 or account.open_escalations >= 2:
            actions.append("Open a cross-functional service recovery plan with support and product owners.")
        if account.product_adoption_score < 55:
            actions.append("Launch a targeted enablement sequence focused on the least-adopted features.")
        if account.payment_delay_days > 20:
            actions.append("Align finance outreach with account management before the next renewal touchpoint.")
        if not actions:
            actions.append("Maintain current success cadence and monitor leading indicators weekly.")

        return {
            "account_id": account.account_id,
            "account_name": account.account_name,
            "risk_band": risk_band(account.churn_risk),
            "recommended_actions": actions,
        }
