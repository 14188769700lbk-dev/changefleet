# Devpost submission draft

## Project name

ChangeFleet

## Tagline

An enterprise agent fleet that turns risky data-contract changes into owner-specific repairs, policy gates, and durable proof.

## Inspiration

A small warehouse schema change can quietly break analytics across repositories and teams. Existing tools usually stop at lineage visualization or code search. We wanted a system that treats the change as an accountable, policy-controlled campaign from discovery through proof.

## What it does

ChangeFleet accepts a proposed schema mutation and coordinates five agents:

- Scout finds affected assets and owners.
- Architect selects a migration strategy based on contract type.
- Repair drafts isolated changes for code-bound assets.
- Govern checks scope, compatibility, and approval policy.
- Proof produces an evidence timeline and final campaign record.

The demo follows `warehouse.orders.shipping_country` through six downstream assets, four repairs, three owners, and one explicit writeback gate. Reviewers can run the complete deterministic flow immediately; configured environments can invoke the live Gemini workflow.

## How we built it

- Google Agent Development Kit 2.7 `Workflow`
- Gemini 3.5 Flash
- Google Cloud Run deployment target
- FastAPI and Pydantic
- React 19, TypeScript, and Vite
- Bounded lineage, contract, owner, repair, and policy tools

## Challenges

The hardest design constraint was keeping a convincing autonomous workflow without making unsafe or unverifiable claims. We separated observed fixture evidence, proposed repairs, local approval, and external mutation into explicit states. The live endpoint also fails closed when credentials are not configured.

## Accomplishments

- Five specialized agents in one auditable workflow
- Contract-aware strategies instead of blind global replacement
- Immediate reviewer mode with no credential requirement
- Responsive mission-control UI with progressive evidence
- Explicit human approval boundary and zero external writeback by default
- Automated backend tests and reproducible frontend build

## What we learned

Agent quality depends as much on bounded tools and state transitions as on prompts. An enterprise system becomes easier to trust when every output says whether it was observed, inferred, proposed, approved, or actually applied.

## What's next

The next milestone is a read-only GitHub and dbt Cloud pilot that imports real lineage and opens draft pull requests only after per-campaign approval. We would then add BigQuery audit export and policy packs for regulated analytics teams.

## Required links before submission

- Public repository: TBD
- Cloud Run demo: TBD
- Demo video: TBD
