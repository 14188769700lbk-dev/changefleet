# Architecture

ChangeFleet separates deterministic evidence handling from model reasoning. The checked-in scenario is the source of truth; agents may interpret it and choose an action, but they cannot invent assets or cross the writeback boundary.

## Runtime paths

| Path | Purpose | Failure behavior |
| --- | --- | --- |
| Fixture engine | Reviewer-ready product flow without credentials | Produces only checked-in synthetic evidence |
| Google ADK workflow | Live Gemini reasoning over the same bounded tools | Returns `503` when credentials are absent |
| Approval endpoint | Records local human approval | `writeback_applied` remains `false` |

## Trust boundary

Read and draft actions are autonomous. External mutation is a separate capability that is not implemented in this public version. Adding GitHub, dbt Cloud, or warehouse writeback later must require short-lived credentials, repository allowlists, per-campaign approval, and an immutable audit record.

## Data flow

1. `scenario_context`, `inspect_lineage`, and `resolve_owners` expose bounded evidence.
2. Scout records the blast radius and accountable teams.
3. Architect looks up contract type and selects direct migration or compatibility preservation.
4. Repair drafts per-file SQL changes.
5. Govern evaluates every action class, blocking unapproved writeback.
6. Proof creates the final record used by the UI timeline.

The FastAPI service owns both the fixture engine and live ADK runner. The React application consumes only the HTTP API and ships as static files in the same Cloud Run container.
