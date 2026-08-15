from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from .models import Asset, ChangeRequest


SCENARIO_PATH = Path(__file__).resolve().parents[2] / "data" / "scenario.json"


@lru_cache(maxsize=1)
def load_scenario() -> tuple[ChangeRequest, tuple[Asset, ...]]:
    payload: dict[str, Any] = json.loads(SCENARIO_PATH.read_text(encoding="utf-8"))
    change = ChangeRequest.model_validate(payload["change"])
    assets = tuple(Asset.model_validate(asset) for asset in payload["assets"])
    return change, assets


def asset_index() -> dict[str, Asset]:
    _, assets = load_scenario()
    return {asset.id: asset for asset in assets}

