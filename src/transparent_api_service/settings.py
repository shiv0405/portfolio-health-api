from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppSettings:
    data_path: Path
    service_name: str
    environment: str

    @classmethod
    def from_env(cls) -> "AppSettings":
        root = Path(__file__).resolve().parents[2]
        default_data = root / "data" / "account_health_snapshot.json"
        configured_path = Path(os.environ.get("PORTFOLIO_HEALTH_DATA_PATH", default_data)).resolve()
        return cls(
            data_path=configured_path,
            service_name="portfolio-health-api",
            environment=os.environ.get("PORTFOLIO_HEALTH_ENV", "local"),
        )
