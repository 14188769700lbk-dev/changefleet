# ChangeFleet paid pilot outline

This is an offer draft, not a claim of an existing customer or validated revenue.

## Ideal buyer

Data platform or analytics engineering teams with 20–200 downstream models, recurring dbt or warehouse migrations, and multiple code owners.

## Four-week pilot

- Week 1: read-only inventory of one warehouse domain and its repositories
- Week 2: lineage, contract, and ownership adapter configuration
- Week 3: shadow-mode change campaigns on historical migrations
- Week 4: one live, human-approved draft pull request and an audit report

## Deliverables

- Blast-radius report for up to three representative changes
- Owner-specific repair drafts
- Policy and approval configuration
- Evidence export and adoption recommendations
- No production write access; draft-only integration by default

## Proposed pricing for discovery

- Design-partner pilot: USD 2,500 fixed, with a clearly bounded scope
- Standard pilot after validation: USD 7,500–12,000 depending on repositories and adapters

These are hypotheses to test in customer conversations, not market facts. Payment terms, taxes, data-processing terms, and security requirements must be agreed before work starts.

## Qualification questions

1. How often do warehouse or semantic-layer changes affect more than one team?
2. What evidence is required before a schema change ships?
3. Where are lineage, ownership, and contracts currently stored?
4. Would a read-only, draft-PR workflow be acceptable for an initial pilot?
5. Who owns the budget for reducing analytics migration risk?
