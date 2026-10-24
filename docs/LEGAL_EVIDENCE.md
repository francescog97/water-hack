# Legal and institutional evidence ledger

## Evidence contract

Technical scenario band != formal disaster declaration != legal trigger != authorization.

All bundled event-specific mappings are **SOURCE_LOCATED_UNREVIEWED**. No domain expert has signed off the current wording, effective version or territorial application. An operator's acknowledgement is recorded as **OPERATOR_ACKNOWLEDGEMENT**, with `legal_authorization=0`. It does not upgrade a source's legal review status.

The default package is `app/config/legalpacks/bulgaria-flood.json`, version 1.0.0. Each source stores publisher, original URL, section, language, retrieval date, version limitations, translation status and reviewer. Effective dates remain null when not independently established. The package SHA-256 is included in the context fingerprint and exported briefing.

## Sources actually consulted — 24 October 2026

| Source | What was located | What remains unverified |
|---|---|---|
| [European Commission: Bulgaria disaster-management system](https://civil-protection-humanitarian-aid.ec.europa.eu/what/civil-protection/national-disaster-management-system/bulgaria_en) | Institutional overview describing national, regional and municipal levels | Exact current statutory provisions, territorial office, event prerequisites and local procedure |
| [MOEW: FRMP 2022–2027 adoption](https://www.moew.government.bg/en/flood-risk-management-plans-for-the-period-2022-2027-have-been-adopted/) | Notice dated 3 January 2024 reporting adoption of plans for four basin districts | Exact applicable plan entry, measure, implementation actor and any local incident trigger |
| [MOEW: Water](https://www.moew.government.bg/en/water/) | National/basin institutional context and flood-planning links | Gauge-to-office crosswalk; case-specific competence or duty |
| [Government-hosted Disaster Protection Act, English PDF](https://www.me.government.bg/en/files/download?hash=a99eb7fec98c348ce4517dac6331c4b9a9596e0c) | Dated English translation. Amendment list ends at SG 80/2011; regional/municipal provisions appear in Articles 64–65 in this copy | Consolidated Bulgarian wording, amendments, exact 2025/2026 effective text, translation and applicability. No current power or deadline is extracted |

The [government landing page](https://www.me.government.bg/en/library/disaster-protection-act-304-c25-m1515-1.html) was accessible. Source existence and current legal applicability are different claims.

## Blocked or unused research leads

- [ISURN description](https://isurn.moew.government.bg/ISURN.Web/BaseProject/homepage/aboutEN.html): retrieval returned HTTP 502. No feature-absence conclusion is drawn.
- [Parliament record 167018](https://www.parliament.bg/en/desision/ID/167018): no readable content returned. The app makes no claim about enactment or effective date.
- A September 2026 proposal, if reviewed later, must not be treated as enacted law. No draft-bill rule is loaded.
- No verified municipal plan, official gauge threshold, evacuation procedure, statutory incident deadline or dam-release power is loaded.
- No national discharge feed is connected. No weather/flow forecast is provided.

## Runtime semantics

The deterministic evaluator checks explicit facts using a three-way state: unknown / reported met / reported unmet. Facts are operator-supplied, not independent evidence. Missing facts and unreviewed sources produce NEEDS_VERIFICATION. A reported-unmet prerequisite is distinguished from an unknown prerequisite.

Changing severity can change the order/emphasis of **review tasks**, but cannot create a legal duty, deadline or power. The bundled `legal_rules` list is empty. No statutory applicability conclusion is issued. All proposed actions are review/information tasks; they are not dispatch instructions.

The coverage matrix describes the loaded package across Authority, Possible measures, Deadlines, Procedures and Legal sources. UNMAPPED means **No verified mapping in the loaded knowledge package**, never that Bulgarian legislation is incomplete. The legend includes VERIFIED, SOURCE_FOUND_REVIEW_PENDING, UNMAPPED, NOT_APPLICABLE and DEMO_ONLY; the bundled records do not fabricate VERIFIED cells.

`bulgaria-source-only.json` is a second real configuration: one institutional source/role, zero procedure mappings. Swapping it reduces package coverage. It is not a fictional legal system.

## Human review handoff

Aliaksei should use LEGAL_REVIEW_CHECKLIST.md. Record the exact provision, source version, territorial scope, effective period, prerequisite and reviewer before creating a reviewed rule. Changing a JSON review label is not a substitute for that work. Formal institutional decisions and signatures are outside this application.
