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
        return cls.from_json_path(dataset_path)

    @classmethod
    def from_json_path(cls, dataset_path: Path) -> "AccountService":
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

    def segment_summary(self) -> dict[str, object]:
        rows: list[dict[str, object]] = []
        for segment in sorted({account.segment for account in self._accounts}):
            matching = [account for account in self._accounts if account.segment == segment]
            rows.append(
                {
                    "segment": segment,
                    "accounts": len(matching),
                    "average_health_score": round(sum(account.health_score for account in matching) / len(matching), 2),
                    "average_churn_risk": round(sum(account.churn_risk for account in matching) / len(matching), 4),
                    "contract_value_usd": int(sum(account.contract_value for account in matching)),
                    "critical_accounts": int(sum(1 for account in matching if risk_band(account.churn_risk) == "critical")),
                }
            )
        rows.sort(key=lambda item: (item["average_churn_risk"], item["contract_value_usd"]), reverse=True)
        return {"segments": rows}

    def high_risk_accounts(self, limit: int = 10, region: str | None = None) -> list[dict[str, object]]:
        accounts = self._accounts
        if region:
            accounts = [account for account in accounts if account.region.lower() == region.lower()]
        ranked = sorted(accounts, key=lambda account: (account.churn_risk, -account.contract_value), reverse=True)
        return [account.to_dict() for account in ranked[:limit]]

    def renewal_forecast(self, horizon_days: int = 120) -> dict[str, object]:
        in_window = [account for account in self._accounts if account.renewal_window_days <= horizon_days]
        rows = [
            {
                "account_id": account.account_id,
                "account_name": account.account_name,
                "region": account.region,
                "segment": account.segment,
                "renewal_window_days": account.renewal_window_days,
                "contract_value": account.contract_value,
                "churn_risk": account.churn_risk,
                "risk_band": risk_band(account.churn_risk),
            }
            for account in sorted(
                in_window,
                key=lambda account: (account.renewal_window_days, -account.churn_risk, -account.contract_value),
            )
        ]
        forecast_value = int(sum(account.contract_value for account in in_window))
        value_at_risk = int(sum(account.contract_value for account in in_window if account.churn_risk >= 0.55))
        return {
            "horizon_days": horizon_days,
            "accounts_in_window": len(in_window),
            "renewal_value_usd": forecast_value,
            "value_at_risk_usd": value_at_risk,
            "accounts": rows,
        }

    def action_queue(self, limit: int = 15, region: str | None = None) -> dict[str, object]:
        accounts = self._accounts
        if region:
            accounts = [account for account in accounts if account.region.lower() == region.lower()]

        queue = []
        for account in sorted(accounts, key=lambda item: (item.churn_risk, item.contract_value), reverse=True):
            recommended_actions = self.recommendations(account.account_id)
            if recommended_actions is None:
                continue
            queue.append(
                {
                    "account_id": account.account_id,
                    "account_name": account.account_name,
                    "region": account.region,
                    "segment": account.segment,
                    "renewal_window_days": account.renewal_window_days,
                    "contract_value": account.contract_value,
                    "health_score": account.health_score,
                    "churn_risk": account.churn_risk,
                    "risk_band": risk_band(account.churn_risk),
                    "priority": self._priority_label(account),
                    "recommended_actions": recommended_actions["recommended_actions"],
                }
            )
        return {
            "generated_items": len(queue),
            "items": queue[:limit],
        }

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

    def _priority_label(self, account: AccountSnapshot) -> str:
        if account.churn_risk >= 0.78 or account.renewal_window_days <= 30:
            return "immediate"
        if account.churn_risk >= 0.55 or account.renewal_window_days <= 60:
            return "near_term"
        return "monitor"
