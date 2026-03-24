from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class ClientConfig:
    api_key: str
    base_url: str = "https://app.scadable.com"
    timeout: float = 30.0
    max_retries: int = 2

    @classmethod
    def resolve(
        cls,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 2,
    ) -> ClientConfig:
        key = api_key or os.environ.get("SCADABLE_API_KEY")
        if not key:
            raise ValueError(
                "No API key provided. Pass api_key= or set SCADABLE_API_KEY."
            )
        url = base_url or os.environ.get(
            "SCADABLE_BASE_URL", "https://app.scadable.com"
        )
        return cls(api_key=key, base_url=url, timeout=timeout, max_retries=max_retries)
