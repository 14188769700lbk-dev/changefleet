from __future__ import annotations

from copy import deepcopy
from threading import Lock

from .fleet_tools import inspect_lineage, resolve_owners
from .models import (
    ApprovalResult,
    Asset,
    CampaignResult,
    CampaignSummary,
    ChangeRequest,
    EvidenceEvent,
    PolicyCheck,
    RepairArtifact,
)
from .scenario import asset_index


class FleetEngine:
    """Deterministic evidence engine used for public replay and policy tests."""

    stages = ["Scout", "Architect", "Repair", "Govern", "Proof"]

    def __init__(self) -> None:
        self._campaigns: dict[str, CampaignResult] = {}
        self._lock = Lock()

    def run(self, change: ChangeRequest) -> CampaignResult:
        graph = inspect_lineage(change.source_asset, change.old_field)
        if graph["status"] != "ok":
            raise ValueError(f"Unknown source asset: {change.source_asset}")

        assets_by_id = asset_index()
        assets = [assets_by_id[asset_id] for asset_id in graph["asset_ids"]]
        repairs = self._build_repairs(change, assets_by_id)
        owners = resolve_owners([repair.asset_id for repair in repairs])
        result = CampaignResult(
            campaign_id=change.change_id,
            state="approval_required",
            change=change,
            assets=assets,
            repairs=repairs,
            policy_checks=self._policy_checks(change),
            events=self._events(len(assets), len(repairs), owners["owner_count"]),
            summary=CampaignSummary(
                affected_assets=len(assets),
                repairs=len(repairs),
                owners=owners["owner_count"],
                approval_gates=1,
            ),
            agent_stages=self.stages,
        )
        with self._lock:
            self._campaigns[result.campaign_id] = result
        return deepcopy(result)

    def approve(self, campaign_id: str) -> ApprovalResult:
        with self._lock:
            campaign = self._campaigns.get(campaign_id)
            if campaign is None:
                raise KeyError(campaign_id)
            campaign.state = "approved"
            # The public demo records approval but intentionally never mutates an external system.
            campaign.writeback_applied = False
        return ApprovalResult(
            campaign_id=campaign_id,
            state="approved",
            writeback_applied=False,
            message="Approval recorded locally; external writeback remains disabled in demo mode.",
        )

    @staticmethod
    def _build_repairs(
        change: ChangeRequest, assets: dict[str, Asset]
    ) -> list[RepairArtifact]:
        old = change.old_field
        new = change.new_field
        return [
            RepairArtifact(
                asset_id="warehouse.orders",
                owner=assets["warehouse.orders"].owner,
                file=assets["warehouse.orders"].file or "",
                strategy="Compatibility alias at the producer",
                current_sql=["SELECT", f"  {old}", "FROM raw.orders"],
                proposed_sql=["SELECT", f"  {new},", f"  {new} AS {old}", "FROM raw.orders"],
                status="contract_preserved",
            ),
            RepairArtifact(
                asset_id="shipping_performance",
                owner=assets["shipping_performance"].owner,
                file=assets["shipping_performance"].file or "",
                strategy="Direct internal migration",
                current_sql=["SELECT", f"  {old},", "  COUNT(*) AS shipments", "FROM warehouse.orders"],
                proposed_sql=["SELECT", f"  {new},", "  COUNT(*) AS shipments", "FROM warehouse.orders"],
                status="patch_ready",
            ),
            RepairArtifact(
                asset_id="revenue_by_market",
                owner=assets["revenue_by_market"].owner,
                file=assets["revenue_by_market"].file or "",
                strategy="Preserve the public output contract",
                current_sql=["SELECT", "  o.order_date,", f"  o.{old} AS country,", "  SUM(o.amount) AS revenue_usd"],
                proposed_sql=["SELECT", "  o.order_date,", f"  o.{new} AS country,", "  SUM(o.amount) AS revenue_usd"],
                status="patch_ready",
            ),
            RepairArtifact(
                asset_id="daily_fulfillment",
                owner=assets["daily_fulfillment"].owner,
                file=assets["daily_fulfillment"].file or "",
                strategy="Direct scheduled-query migration",
                current_sql=["SELECT order_id", f"WHERE {old} IS NOT NULL"],
                proposed_sql=["SELECT order_id", f"WHERE {new} IS NOT NULL"],
                status="patch_ready",
            ),
        ]

    @staticmethod
    def _policy_checks(change: ChangeRequest) -> list[PolicyCheck]:
        return [
            PolicyCheck(
                policy="bounded_lineage",
                outcome="passed",
                evidence="Traversal is limited to registered downstream edges.",
            ),
            PolicyCheck(
                policy="repository_scope",
                outcome="passed",
                evidence="Drafts target only registered repository bindings.",
            ),
            PolicyCheck(
                policy="contract_preservation",
                outcome="passed",
                evidence=f"Public outputs retain {change.old_field} while reading {change.new_field}.",
            ),
            PolicyCheck(
                policy="external_writeback",
                outcome="approval_required",
                evidence="No external mutation can execute without explicit approval.",
            ),
        ]

    @staticmethod
    def _events(asset_count: int, repair_count: int, owner_count: int) -> list[EvidenceEvent]:
        return [
            EvidenceEvent(
                stage="Scout",
                title="Lineage graph loaded",
                detail=f"All {asset_count} affected assets discovered.",
                offset_seconds=0,
            ),
            EvidenceEvent(
                stage="Scout",
                title=f"{owner_count} owners resolved",
                detail="Owners mapped to every code-bound asset.",
                offset_seconds=4,
            ),
            EvidenceEvent(
                stage="Repair",
                title=f"{repair_count} repairs generated",
                detail="Owner-specific patches created for impacted assets.",
                offset_seconds=15,
            ),
            EvidenceEvent(
                stage="Govern",
                title="Policy gate passed",
                detail="Scope and contract-preservation checks satisfied.",
                offset_seconds=26,
            ),
            EvidenceEvent(
                stage="Proof",
                title="Approval required for writeback",
                detail="External mutation remains blocked pending human approval.",
                offset_seconds=33,
                status="approval_required",
            ),
        ]

