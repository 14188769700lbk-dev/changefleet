# 90-second demo script

## 0:00–0:12 — Problem

“One warehouse field rename can break models, dashboards, and executive metrics across several owners. ChangeFleet turns that change into one governed campaign.”

Show the source and change strip: `shipping_country → country_code`.

## 0:12–0:35 — Fleet

Click **Run coordinated repair**. As the rail advances, explain Scout, Architect, Repair, Govern, and Proof. Point out that evidence appears progressively rather than as an instant canned result.

## 0:35–0:58 — Contract-aware result

Click `revenue_by_market`. Show the side-by-side repair preserving the public `country` output while changing the upstream reference to `country_code`. Contrast it with internal direct migrations.

## 0:58–1:15 — Safety

Open **Architecture**. Explain the read-only tools and mutation boundary. Close it and point to the vermilion approval-required event.

## 1:15–1:30 — Proof and platform

Click **Approve writeback**. Explain that the demo records human approval but deliberately performs no external mutation. Close on the Google ADK five-agent workflow, Gemini 3.5 Flash, and Cloud Run deployment target.
