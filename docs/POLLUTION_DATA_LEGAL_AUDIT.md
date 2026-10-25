# Suspected river pollution: data and procedure audit

Research date: 25 October 2026. This audit supports the Aliaksei report's first product: a complete, reviewable suspected-pollution case on one short Bulgarian river reach. It does not establish an actual incident, violation, statutory deadline or authority instruction. Expert legal, laboratory and territorial sign-off is **pending**.

## Data that can truthfully be used

All **172 originals** in `Dataset/registro_rinomine.csv` were read and their SHA-256 values checked against that manifest during this audit: **zero mismatches**. No original was edited.

| Local input | Verified content | Permitted demonstration use / limitation |
|---|---|---|
| `surfacewater Bulgaria_weak/sostanze_sospese.csv` | 9,657 observations; `date,value(mg/l)`; 2019-01-03 10:50 to 2024-12-16 16:30; min 2, median 7.2, max 1,998 mg/L; 784 rows repeat a timestamp | Dataset inspection and pooled distribution only. Missing station, coordinates, sample ID, method, qualification and uncertainty prevent attribution to an Iskar reach or treating it as one station's baseline. Suspended solids are not a turbidity measurement. |
| Surface-water `best` and `weak` chemistry | 39 and 28 CSVs, respectively; 2019–2024; date/value/unit | Retain parameter and source file. Neither folder name establishes water status. Do not join by timestamp or infer matching samples. Dissolved and total concentrations are different measurands. |
| Groundwater chemistry | 22 CSVs; 2018–2024; missing station/sample/location | Groundwater catalogue only; cannot support a specific river incident. |
| CDS precipitation June 1–3 2024 CSV | 1,890 `lon,lat,value` rows; matching collection describes EPSG:4326, 0.1° cells, `tp`, metres | Optional historical geographic context. Conversion to mm is multiplication by 1,000; temporal aggregation is unknown. This is not a rainfall forecast, observed pollutant or proof of runoff causation. |
| CDS soil moisture | `swvl1`, m³/m³; 0.1° grid; 2024 | Historical context only; layer depth and aggregation insufficiently documented. Missing cells are not zero. |
| GEE rasters | Georeferenced precipitation and soil grids; 2024 and a precipitation period in 2026 | Units/product/aggregation not declared locally; exclude physical interpretation until recovered. |
| Iskar discharge | Novi Iskar and Orehovitsa; 146 dated observations per file, July–December 2025; m³/s | Separate historical flow replay. No time/location join to the 2019–2024 chemistry or 2024 climate layers. |
| Danube / Arda | Danube level/temperature 2021; reservoir bulletins 2017 | Separate historical collections; exclude from the pollution case. Gauge level in cm is not depth. |

TSS file SHA-256: `081e752084f0906b5e03f3f0e7cff8daf70ea3b8505e2f3b17fbb9b8c31aef4c`.

CDS June 1–3 precipitation CSV SHA-256: `33330f47e017567b019839f2da77a1abedc0ac274cffb97ab7a22d343be2cf93`.

The illustrative nearest grid centre to approximately 23.35°E, 42.8°N is 23.4°E, 42.8°N, with stored value 0.035417404025793076 m (35.417404025793076 mm). This is a grid-cell value with unknown aggregation, not a gauge observation at the scenario station. The collection name alone does not certify product provenance or licence. See the collection READMEs for other metadata limitations.

## Exact safe fallback plan

Use a **synthetic suspected-pollution exercise around Novi Iskar**, explicitly distinct from historical incidents. Invented reach vertices, upstream/downstream direction, sample locations, receptors and possible discharge points must all carry `DEMO_SYNTHETIC`. Approximate coordinates are illustrative, not surveyed river geometry, jurisdiction boundaries or actual infrastructure. No named business is accused of a discharge.

Use demonstrative laboratory inputs in **mg/L of suspended solids**: for example an invented baseline of 8 mg/L and an invented elevated sample of 96 mg/L, with distinct sample IDs and explicit timestamps. These values are constructed examples, not extracted observations or issued laboratory reports. A configured anomaly threshold, if used, is a demonstration setting with no statutory or operational significance; no numeric value in this audit is an environmental quality standard. Record the final configured threshold and comparator in the rulepack and briefing. Never compare suspended-solids mg/L to turbidity NTU or infer PFAS, metals, pesticides, toxicity or a responsible polluter from colour or imagery.

Keep actual CDS raster/CSV context dated **2024-06-01 / 2024-06-03**. If the synthetic scenario uses that period, coincidence of dates is part of the exercise and does not validate causal linkage. If it uses another period, label the layer as separate historical context and exclude it from incident evidence scoring. Satellite/geospatial observations can support a verification question; they cannot independently identify a pollutant. A schematic reach is not itself an open geospatial data source: retain the actual local geographic cell provenance where used.

The packaged scenario is `app/config/incidents/iskar-pollution-demo.json`: baseline 8 mg/L, sample 96 mg/L (12×), configured display trigger **30 mg/L with comparator `>=`**, all explicitly synthetic. This trigger was chosen for a visible exercise transition and has no statutory, calibrated or operational meaning.

The output should say **suspected anomaly; pollution cause unconfirmed; proposed verification plan; human approval pending**. A user acknowledging a case does not become a laboratory or legal expert and does not upgrade source review status. Proposed verification/notification drafts remain reviewable records; this demo sends nothing externally.

For real-data replacement, require a station/water-body ID, coordinates and CRS, time zone, sample ID, parameter and fraction, units, method, LOQ/qualifiers, uncertainty, laboratory provenance and chain of custody, plus current authority crosswalk, permits and reviewed event procedure. Unknown fields stay unknown. Recover these from original providers before joining existing chemistry to the map.

## Sources located and precise verification limits

| ID | Primary source / located record | Verification and permitted scope |
|---|---|---|
| `moew-water` | [MOEW Water institutional overview](https://www.moew.government.bg/en/water/) | Page retrieved. Institutional orientation only; no event-specific competence, order or deadline verified. |
| `riew-iskar-case` | [RIEW Sofia news archive](https://riew-sofia.org/index.php/2014-02-03-21-15-52), item on Kurilo dated 13.05.2025 | Official historical record: joint inspection involving RIEW Sofia, Danube Basin Directorate and environmental-agency sampling; field screening did not resolve every concern. Supports a candidate coordination route, not a universal legal procedure. Bulgarian paraphrase; translation and present applicability unreviewed. |
| `moew-natural-cause` | [MOEW Iskar/Mezdra investigation, 25 June 2015](https://www.moew.government.bg/bg/signal-za-zamursyavane-na-reka-iskur-v-rajona-na-mezdra-proveri-riosv-vraca/) | Official historical report links brown, turbid water to rain-activated earth movement and reports laboratory involvement. Supports considering a natural cause; it is not evidence about today's exercise. |
| `eu-lab-quality` | [Commission Directive 2009/90/EC, Articles 3 and 6](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32009L0090) | EUR-Lex indexed official text located: validated/documented methods and laboratory quality assurance for WFD chemical monitoring. Direct HTML/PDF opens hit an anti-bot page; full current consolidation and Bulgarian implementation **not verified**. No incident-specific obligation is loaded. |
| `riew-contact` | [RIEW Sofia official homepage](https://www.riew-sofia.org/) | Reporting/contact information located. A human must reconfirm the current channel and territorial remit before sending anything. No contact is automatically used. |

All source and proposed-procedure mappings remain `SOURCE_LOCATED_UNREVIEWED`, `reviewer=null`, effective dates unknown unless subsequently independently established. Source retrieval does not constitute professional sign-off.

## Five proposed, source-backed steps

These are application review tasks inferred from the located records, **not five legally verified rules**. Owners are proposed role assignments, not actual public officials or assumed powers. Each task has no verified statutory deadline (`deadline_value=null`, `deadline_type=NONE_VERIFIED`).

| Step | Proposed owner / dependency | Evidence and reviewable result |
|---|---|---|
| 1. Check anomaly provenance and competing explanations | Environmental analyst; starts the case | Record sample/units/time/location gaps and preserve original evidence. Consider sediment mobilisation as well as a discharge hypothesis. Source: `moew-natural-cause`. |
| 2. Confirm territorial routing and contacts | Authorised technical specialist; after location check | Confirm the specific reach, basin and inspectorate. Danube Basin Directorate and RIEW Sofia are candidates supported by `moew-water` and `riew-iskar-case`; current case routing stays pending. |
| 3. Draft a field/laboratory verification request | Laboratory liaison; after routing review | Request a sampling design and appropriate analysis from qualified specialists. Proposed upstream/event/downstream points, sample IDs and custody fields are product-design suggestions requiring approval; method/QA review refers to `eu-lab-quality`. |
| 4. Prepare an evidence-linked notification draft | Assigned case coordinator; after recipient confirmation | Include location, times, observed facts, demo labels and unknowns; retain as a draft. Sources: `riew-iskar-case`, `riew-contact`. No send, enforcement action or liability finding occurs. |
| 5. Review results and approve next steps | Authorised specialist and approving manager; after results and legal check | Log interpretation, source version, applicability check, decision and follow-up. Route unresolved concerns back for verification. Source context: `riew-iskar-case`, `eu-lab-quality`; the approval gate is a product safeguard. |

Pending professional checks: current Bulgarian Water Act and secondary rules; applicable site permit and receiving-water criteria; exact reach jurisdiction; sampling standards and laboratory authority; any notification prerequisites/recipients/deadlines; authorisation for measures; current EU amendments/transposition. No drinking-water limit is transferred to a river suspended-solids trigger. Environmental Liability Directive Articles 5–6, AI Act, PFAS and later DOCX policy claims are research leads outside this narrow procedure pack; none is asserted applicable or enacted solely because the report cites it.

The demonstrator can satisfy the report's 3–5 **source-backed proposed steps** target. Its target of expert-verified event-specific legal mappings remains **pending expert review**, and must remain visible in the app and presentation.
