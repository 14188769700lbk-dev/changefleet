from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ChangeRequest(BaseModel):
    change_id: str = "CF-204"
    source_asset: str = "warehouse.orders"
    old_field: str = "shipping_country"
    new_field: str = "country_code"
    reason: str = "Standardize ISO country identifiers"


class Asset(BaseModel):
    id: str
    label: str
    kind: str
    owner: str
    criticality: Literal["tier_1", "tier_2", "tier_3"]
    contract: Literal["producer", "internal", "public_output", "observed_only"]
    file: str | None = None
    downstream: list[str] = Field(default_factory=list)


class EvidenceEvent(BaseModel):
    stage: Literal["Scout", "Architect", "Repair", "Govern", "Proof"]
    title: str
    detail: str
    offset_seconds: int
    status: Literal["verified", "observed", "approval_required"] = "verified"


class RepairArtifact(BaseModel):
    asset_id: str
    owner: str
    file: str
    strategy: str
    current_sql: list[str]
    proposed_sql: list[str]
    status: Literal["patch_ready", "contract_preserved"]


class PolicyCheck(BaseModel):
    policy: str
    outcome: Literal["passed", "blocked", "approval_required"]
    evidence: str


class CampaignSummary(BaseModel):
    affected_assets: int
    repairs: int
    owners: int
    approval_gates: int


class CampaignResult(BaseModel):
    campaign_id: str
    state: Literal["approval_required", "approved"]
    change: ChangeRequest
    assets: list[Asset]
    repairs: list[RepairArtifact]
    policy_checks: list[PolicyCheck]
    events: list[EvidenceEvent]
    summary: CampaignSummary
    agent_stages: list[str]
    writeback_applied: bool = False


class ApprovalResult(BaseModel):
    campaign_id: str
    state: Literal["approved"]
    writeback_applied: bool
    message: str


class AgentRunRequest(BaseModel):
    prompt: str = (
        "Coordinate the CF-204 change from shipping_country to country_code "
        "and return an evidence-grounded migration plan."
    )
    user_id: str = "demo-reviewer"

