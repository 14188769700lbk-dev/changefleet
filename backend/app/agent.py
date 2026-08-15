from __future__ import annotations

import os

from google.adk.agents import LlmAgent
from google.adk.workflow import START, Workflow

from .fleet_tools import (
    draft_repair,
    evaluate_policy,
    inspect_lineage,
    lookup_contract,
    resolve_owners,
    scenario_context,
)


MODEL = os.getenv("CHANGEFLEET_MODEL", "gemini-3.5-flash")

scout_agent = LlmAgent(
    name="scout",
    model=MODEL,
    description="Discovers the bounded blast radius and accountable owners.",
    instruction=(
        "You are ChangeFleet Scout. Inspect the provided schema change with the tools. "
        "Return only evidence-backed affected assets, edges, and code-owning teams. "
        "Never invent an asset or repository."
    ),
    tools=[scenario_context, inspect_lineage, resolve_owners],
    output_key="impact_report",
)

architect_agent = LlmAgent(
    name="architect",
    model=MODEL,
    description="Selects an owner-specific, contract-safe migration sequence.",
    instruction=(
        "You are ChangeFleet Architect. Use {impact_report} and contract lookups to choose "
        "a compatibility policy for each code-bound asset. Preserve public outputs, prefer "
        "direct migration for internal consumers, and explain the dependency order."
    ),
    tools=[lookup_contract],
    output_key="migration_plan",
)

repair_agent = LlmAgent(
    name="repair",
    model=MODEL,
    description="Drafts isolated repository repairs from the approved migration plan.",
    instruction=(
        "You are ChangeFleet Repair. Follow {migration_plan}. Call draft_repair for every "
        "code-bound asset and report exact files and strategies. Draft only; do not claim "
        "a pull request or external write."
    ),
    tools=[draft_repair],
    output_key="repair_manifest",
)

govern_agent = LlmAgent(
    name="govern",
    model=MODEL,
    description="Enforces scope, contract, and mutation policies.",
    instruction=(
        "You are ChangeFleet Govern. Validate {repair_manifest} against the migration plan. "
        "Use evaluate_policy for inspect, draft, validate, and writeback actions. Any "
        "writeback without explicit approval must remain approval_required."
    ),
    tools=[evaluate_policy],
    output_key="governance_report",
)

proof_agent = LlmAgent(
    name="proof",
    model=MODEL,
    description="Produces the final auditable campaign record.",
    instruction=(
        "You are ChangeFleet Proof. Combine {impact_report}, {migration_plan}, "
        "{repair_manifest}, and {governance_report} into a concise evidence record. "
        "Separate observed facts from proposed actions and state the approval boundary."
    ),
    output_key="campaign_record",
)

agent_stages = [
    scout_agent,
    architect_agent,
    repair_agent,
    govern_agent,
    proof_agent,
]

root_agent = Workflow(
    name="changefleet",
    description="Coordinates a five-stage, policy-gated enterprise data change campaign.",
    edges=[
        (START, scout_agent),
        (scout_agent, architect_agent),
        (architect_agent, repair_agent),
        (repair_agent, govern_agent),
        (govern_agent, proof_agent),
    ],
)
