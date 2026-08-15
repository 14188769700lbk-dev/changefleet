from __future__ import annotations

from collections import deque
from typing import Any

from .scenario import asset_index, load_scenario


def inspect_lineage(source_asset: str, field: str) -> dict[str, Any]:
    """Return the bounded downstream graph for a proposed field change."""
    assets = asset_index()
    if source_asset not in assets:
        return {"status": "not_found", "source_asset": source_asset, "field": field}

    visited: set[str] = set()
    queue: deque[str] = deque([source_asset])
    ordered: list[str] = []
    edges: list[dict[str, str]] = []
    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        ordered.append(current)
        for downstream in assets[current].downstream:
            edges.append({"from": current, "to": downstream})
            if downstream not in visited:
                queue.append(downstream)

    return {
        "status": "ok",
        "source_asset": source_asset,
        "field": field,
        "asset_ids": ordered,
        "edges": edges,
        "coverage": "complete_for_fixture",
    }


def resolve_owners(asset_ids: list[str]) -> dict[str, Any]:
    """Resolve accountable owners only for assets that require code changes."""
    assets = asset_index()
    owners: dict[str, list[str]] = {}
    for asset_id in asset_ids:
        asset = assets.get(asset_id)
        if asset is None or asset.file is None:
            continue
        owners.setdefault(asset.owner, []).append(asset.id)
    return {"owners": owners, "owner_count": len(owners)}


def lookup_contract(asset_id: str) -> dict[str, Any]:
    """Return the contract policy that determines a repair strategy."""
    asset = asset_index().get(asset_id)
    if asset is None:
        return {"status": "not_found", "asset_id": asset_id}
    return {
        "status": "ok",
        "asset_id": asset.id,
        "contract": asset.contract,
        "criticality": asset.criticality,
        "owner": asset.owner,
        "file": asset.file,
    }


def draft_repair(asset_id: str, old_field: str, new_field: str) -> dict[str, Any]:
    """Draft a bounded repair for a known repository binding."""
    asset = asset_index().get(asset_id)
    if asset is None:
        return {"status": "not_found", "asset_id": asset_id}
    if asset.file is None:
        return {
            "status": "observed_only",
            "asset_id": asset.id,
            "reason": "No code binding is registered for this asset.",
        }

    if asset.contract == "producer":
        strategy = "Add the replacement field and preserve a compatibility alias."
    elif asset.contract == "public_output":
        strategy = "Read the replacement field while preserving the public output alias."
    else:
        strategy = "Migrate the internal reference directly to the replacement field."
    return {
        "status": "drafted",
        "asset_id": asset.id,
        "file": asset.file,
        "owner": asset.owner,
        "strategy": strategy,
        "old_field": old_field,
        "new_field": new_field,
    }


def evaluate_policy(action: str, target: str) -> dict[str, Any]:
    """Enforce the mutation boundary used by every ChangeFleet agent."""
    allowed_read_actions = {"inspect", "plan", "draft", "validate"}
    if action in allowed_read_actions:
        return {
            "outcome": "passed",
            "action": action,
            "target": target,
            "reason": "Read and isolated-draft actions are permitted.",
        }
    return {
        "outcome": "approval_required",
        "action": action,
        "target": target,
        "reason": "External writeback requires an explicit human approval token.",
    }


def scenario_context() -> dict[str, Any]:
    """Return the fixture change and assets for a reproducible agent run."""
    change, assets = load_scenario()
    return {
        "change": change.model_dump(),
        "assets": [asset.model_dump() for asset in assets],
    }

