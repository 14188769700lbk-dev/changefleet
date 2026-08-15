export type StageName = "Scout" | "Architect" | "Repair" | "Govern" | "Proof";

export interface ChangeRequest {
  change_id: string;
  source_asset: string;
  old_field: string;
  new_field: string;
  reason: string;
}

export interface Asset {
  id: string;
  label: string;
  kind: string;
  owner: string;
  criticality: "tier_1" | "tier_2" | "tier_3";
  contract: "producer" | "internal" | "public_output" | "observed_only";
  file: string | null;
  downstream: string[];
}

export interface EvidenceEvent {
  stage: StageName;
  title: string;
  detail: string;
  offset_seconds: number;
  status: "verified" | "observed" | "approval_required";
}

export interface RepairArtifact {
  asset_id: string;
  owner: string;
  file: string;
  strategy: string;
  current_sql: string[];
  proposed_sql: string[];
  status: "patch_ready" | "contract_preserved";
}

export interface CampaignResult {
  campaign_id: string;
  state: "approval_required" | "approved";
  change: ChangeRequest;
  assets: Asset[];
  repairs: RepairArtifact[];
  policy_checks: Array<{
    policy: string;
    outcome: "passed" | "blocked" | "approval_required";
    evidence: string;
  }>;
  events: EvidenceEvent[];
  summary: {
    affected_assets: number;
    repairs: number;
    owners: number;
    approval_gates: number;
  };
  agent_stages: StageName[];
  writeback_applied: boolean;
}

