# Water Crisis Decision Navigator: a defensible hackathon story

Basis: Aliaksei's expert report dated 25 October 2026, especially sections 4, 7 and 9. This is a presentation narrative and validation plan, not evidence of customer demand or financial performance.

## Nine-slide narrative

1. **The decision gap.** Monitoring signals, laboratory records, permits and institutional procedures must be assembled into a justified response. Fragmentation and coordination delays are interview hypotheses, not proven deficiencies of named organisations.
2. **One first user story.** An environmental analyst investigates a constructed elevated suspended-solids sample on one schematic Bulgarian river reach. The demo's mg/L values are not turbidity in NTU or an actual laboratory result. An anomaly is not proof of pollution, a specific pollutant, a legal breach or liability. Show timestamp, origin, uncertainty and missing corroborating measurements.
3. **From observation to reviewed action.** Locate potentially affected receptors; propose a competent authority; retrieve reviewed, versioned applicable procedures; draft checks and notifications; obtain specialist approval; record assignments, evidence and decisions. National jurisdiction and permit applicability require expert validation.
4. **Who uses it and who pays?** Start with one River Basin Directorate as expert design partner and one utility or industrial operator as a potential paying pilot. Officers, dispatchers and EHS specialists use the workflow; directors sponsor adoption; authorised public budget holders or companies authorise expenditure. Include IT, cybersecurity, legal and procurement in discovery. No organisation has committed to a pilot or purchase.
5. **Compete honestly.** Existing providers already deliver maps, alerts, operational intelligence and workflows. The hypothesis is the specialised connection between water hazards, verifiable legal duties, jurisdiction, expert-approved procedure and a traceable record. Integrate admissible data and existing systems rather than building a universal forecasting platform.
6. **Illustrate value without promising it.** Present the three calculations below with adjustable assumptions. Released capacity is not necessarily cash savings; avoided loss is unproven.
7. **Show a measurable pilot design.** Compare equivalent decision-preparation tasks with and without the MVP. Collect actual elapsed minutes, expert checks of jurisdiction and legal citations, action completeness and user understanding. Targets are at least 30% less time, zero critical jurisdiction errors, all checked citations correct and applicable, explicit uncertainty and appropriate human approval. None is an achieved outcome without evidence.
8. **Test demand.** Propose an initial 8–10 interviews, obtain permission for anonymised reports and controlled workflow observation, and ask who could approve a paid pilot and from which budget. Relevant staff and data commitments are meaningful signals; even budget discussions are not a contract.
9. **Ask for a narrow next step.** Seek an expert partner and a scoped 2–3 month paying pilot covering one territory, one incident type, defined data and reviewed procedures. Scope setup, integrations and support separately. Floods, droughts, industrial safety, insurance and additional countries are roadmap modules.

## Competitor comparison

Public descriptions initially summarised from the supplied report; the bounded primary-source check below records what was subsequently checked and its limitations. This is not a complete technical audit, procurement assessment or independent verification of the supplied report. “Not established” means this comparison has not established a capability, never that a provider lacks it.

| Provider and primary source | Established description in the report | Relationship |
| --- | --- | --- |
| [Copernicus EMS](https://emergency.copernicus.eu/about/) | Flood forecasting, satellite monitoring and crisis / damage mapping | Data input and alternative monitoring capability |
| [FloodMapp](https://www.floodmapp.com/) | Flood depths and footprints; impacts on roads, properties and infrastructure; operational support | Direct flood-response competitor |
| [Fathom](https://www.fathom.global/sector/insurance/) | Flood hazard, asset and portfolio assessment, insurance models and APIs | Strong insurance analytics competitor |
| [EOMAP eoapp AQUA](https://eomap.com/start-download/eoapp-aqua-leaflet) | Satellite water-quality indicators, trends, thresholds and notifications | Closest pollution-monitoring competitor |
| [ArcGIS Workflow Manager](https://doc.esri.com/en/arcgis-workflow-manager/latest/help/an-introduction-to-arcgis-workflow-manager.html) | Task sequences, assignments, roles and notifications | Existing GIS workflow capability |

A Bulgarian legal / jurisdiction workflow is **not established in this comparison** for each provider. Do not claim that competitors only show maps, that satellite alerting is unique, or that map + tasks + notifications is novel.

### Primary-source claim ledger — checked 25 October 2026

The check concerns the existence of publicly described capabilities, not their accuracy, performance, commercial availability for a Bulgarian deployment or the completeness of the report. Product descriptions are vendor claims. No product was purchased, technically audited or compared on a common benchmark.

| Primary page and retrieval status | Bounded finding supporting the app / pitch | Limits |
| --- | --- | --- |
| [Copernicus EMS: About](https://emergency.copernicus.eu/about/) — full page retrieved | Describes EFAS/GloFAS forecasts, near-real-time flood monitoring and on-demand mapping for preparedness, response and recovery. | On-demand activation is restricted to authorised users; free public products do not imply unrestricted activation rights or a verified integration. |
| [FloodMapp](https://www.floodmapp.com/) — full page retrieved | Describes forecast flood locations/depths, affected roads/assets/communities, evacuation support, damage assessment and GIS integration. | Confirms substantial operational decision support. No claim here establishes local coverage, performance, price or Bulgarian legal workflow. |
| [Fathom: insurance](https://www.fathom.global/sector/insurance/) — full page retrieved | Describes flood maps, property/multiple-location exposure, risk scores delivered through an API and portfolio catastrophe models. | Supports insurance analytics positioning; no independent validation of model quality, loss avoidance or commercial terms was performed. |
| [EOMAP water quality](https://eomap.com/services/water-quality/), [eoapp AQUA launch](https://eomap.com/press-release_eoapp-aqua-launch/) and [eoapp AQUA](https://eoapp.de/) — primary-site text available through search indexing; direct full-content retrieval incomplete | Indexed EOMAP descriptions identify satellite-derived water-quality information, historical/current monitoring, time series and threshold-based alerts. The product-site index describes email notifications. | The report's [leaflet endpoint](https://eomap.com/start-download/eoapp-aqua-leaflet) and direct EOMAP service/launch fetches timed out; some other EOMAP pages returned 403; direct product-page extraction was empty. This is a partial primary-source check, not confirmation of the present downloadable leaflet or a fresh complete page inspection. |
| [Esri: Workflow Manager introduction](https://doc.esri.com/en/arcgis-workflow-manager/latest/help/an-introduction-to-arcgis-workflow-manager.html) — full page retrieved | Describes configurable steps/jobs, assignment to people/groups, email notifications, document approvals and roles/privileges controlling the UI. | Existing generic GIS and non-GIS workflow capability is clear. No Bulgarian water-law configuration was established or ruled out. |

The nine-slide Italian HTML pitch at `app/frontend/public/presentation.html` is consistent with these bounded findings: slide 5 presents existing capability and a specialisation hypothesis, without asserting that competitors lack legal or territorial functionality. The Pilot & Value descriptions therefore need no wording changes from this check. Its original EOMAP leaflet link is retained as the report's reference; the additional accessible/indexed primary references and retrieval caveat are recorded above.

### 2026 law and policy claims: excluded from this pitch

The current Navigator, Pilot & Value screen and nine-slide HTML pitch do **not** use the report's claims about Directive (EU) 2026/805, January 2026 drinking-water PFAS changes, AI Act implementation dates, the Water Resilience Investment Accelerator or a funding deadline. They also omit the report's EU loss totals and funding-gap figures. These claims were not independently verified in this competitor check and must not be presented as checked findings. The screen's statement that the demonstration has no PFAS result is an evidence limitation, not a claim about a 2026 legal requirement.

Existing directive links in the incident's candidate source cards are review starting points; this ledger does not validate their national implementation, exact applicable provisions, site permits or authority assignments. No finding here establishes the product's legal compliance.

## Report economics: illustrative assumptions only

These are neither quotations nor validated savings, customer statistics, actuarial forecasts or guaranteed ROI. Annualised implementation cost allocates setup over three years; this is not a payback-period calculation.

| Scenario | Modelled annual benefit | Annualised cost | Modelled annual net benefit |
| --- | --- | --- | --- |
| River Basin Directorate | 120 hours/month × €35/hour × 35% × 12 = **€17,640** | €12,000 + €6,000 / 3 = **€14,000** | **€3,640** |
| Industrial enterprise | 100 × €40 × 30% × 12 + (30% × €120,000 × 20%) = €14,400 + €7,200 = **€21,600** | €14,000 + €6,000 / 3 = **€16,000** | **€5,600** |
| Insurer | 500 comparable assets × 2% annual event probability × €20,000 covered loss × 10% hypothetical loss reduction = **€20,000** | **€25,000** annual fee | **−€5,000** |

The insurer example does not support a positive return. It ignores correlated losses, policy terms, deductibles and measures already in place. Industrial loss reduction is unobserved; first evaluate time, response speed and procedural accuracy. Do not promise a percentage reduction in claims or attribute all avoided damage to this platform.

### Illustrative startup contribution (report §7.8; alignment audit B07)

Assumed annual customer revenue **€18,000** − annual variable cost **€3,000** = **€15,000 contribution per customer**. Assumed annual fixed company cost **€120,000** / **€15,000** = **8 customers** to cover those modelled costs. At eight customers, modelled revenue and total costs are both €144,000.

This is arithmetic under illustrative assumptions, not a sales forecast or proof of business viability. It excludes material uncertainties: lengthy public-sector sales processes, commercial-data subscriptions, delayed payments, churn, taxes and the extra cost of adapting the legal layer to new countries. Source trace: expert report §7.8, requirement **B07** in [the alignment audit](ALIAKSEI_ALIGNMENT.md).

## Interview plan and evidence request

Proposed, not conducted: 2 River Basin professionals, 2 regional environmental specialists, 2 utility staff, 1–2 industrial specialists, 1 insurer, 1 IT/procurement officer. This role allocation totals **9 to 10 interviews**, within the proposed round. Do not present these as completed interviews.

Ask about a recent real alert, tools used, elapsed time, approval steps, hand-offs, serious errors, current contracts and budget authority. Request permission for an anonymised incident report, a relevant permit excerpt, procedure and controlled task observation. Availability is unconfirmed. Never obtain operational data without authorisation.

The Pilot & Value screen starts comparison fields empty and exports explicitly entered numbers as **self-reported**, not independently validated. An entry is not evidence that a customer pilot occurred. A comparable-task study needs identified task design, review methodology and retained evidence outside this demonstrator before performance claims can be substantiated.

## Presentation discipline

Use “demonstrator”, “proposed”, “hypothesis”, “illustrative” and “requires expert review” where appropriate. Distinguish implemented software behaviour from verified national legal content, reviewed scientific inference, real customer research and production readiness. Test results prove specified software behaviour, not market demand, legal correctness or environmental impact.

