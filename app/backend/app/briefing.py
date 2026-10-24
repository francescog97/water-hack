from datetime import datetime, timezone

from .review import list_reviews


def make_briefing(evaluation: dict, review_ids: list[int], *, review_records: list[dict] | None = None) -> dict:
    records = {r["id"]: r for r in (list_reviews(evaluation["context_id"]) if review_records is None else review_records)}
    if not review_ids or any(i not in records for i in review_ids):
        raise ValueError("Acknowledge this exact scenario before export. Data, rules, facts or package changes require a new review.")
    reviews = [records[i] for i in dict.fromkeys(review_ids)]
    result = {
        "title": "Crisis2Action · UNAPPROVED DRAFT INCIDENT BRIEFING",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "context_id": evaluation["context_id"], "official_authorization": False,
        "warning": "DEMONSTRATION · NOT FOR OPERATIONAL USE. Operator acknowledgement is not expert legal verification or an institutional decision.",
        "mode": evaluation["effective_mode"], "station": evaluation["case"]["station"],
        "selected_historical_date": evaluation["request"]["selected_date"],
        "historical_observation": evaluation["observation"],
        "scenario_classification": evaluation["classification"],
        "scenario": evaluation["simulation"], "assumptions": evaluation["simulation_assumptions"],
        "scenario_applied": bool(evaluation["simulation"]),
        "rules": evaluation["rule_pack"],
        "legal_package": {k: evaluation["legal_pack"][k] for k in ("id", "version", "content_sha256")},
        "response_review": evaluation["response"], "coverage": evaluation["coverage"],
        "source_ledger": [evaluation["case"]["source"], *evaluation["legal_pack"]["sources"]],
        "limitations": evaluation["warnings"], "operator_acknowledgements": reviews,
    }
    lines = [f"# {result['title']}", "", result["warning"], "",
             f"Mode: {result['mode'].upper()}. Historical anchor: {result['selected_historical_date']}.",
             f"Station: {result['station']['name']} · Iskar · Bulgaria.",
             f"Parameter: discharge (m3/s). Scenario band: {result['scenario_classification']['band']} — DEMO RISK RULE.",
             f"Historical value: {evaluation['observation']['value'] if evaluation['observation'] else 'UNAVAILABLE'} m3/s.",
             f"Scenario value: {evaluation['effective_value'] if evaluation['effective_value'] is not None else 'UNAVAILABLE'} m3/s.",
             f"Context: {result['context_id']}", "", "## Evidence and limits", *[f"- {w}" for w in result["limitations"]],
             "", "## What-if assumptions", f"Linear increase: {result['assumptions']['daily_increase']} m3/s per day for {result['assumptions']['steps']} day steps. Not a forecast." if result["scenario_applied"] else "No synthetic trajectory was applied. Configured what-if parameters are retained as metadata only; no forecast is available.",
             "", "## Institutional review tasks"]
    for card in result["response_review"]["cards"]:
        lines.extend([f"- {card['title']} — {card['evaluation']}; {card['deadline_display']}", f"  {card['notes']}"])
    lines.extend(["", "## Sources"])
    for source in result["source_ledger"]:
        lines.append(f"- {source.get('source_title', source.get('title'))}: {source.get('official_url', source.get('path'))}")
        if source.get("article_or_section"):
            lines.append(f"  {source['article_or_section']} · {source['version_or_last_verified']} · {source['review_status']}")
    lines.extend(["", "## Human review — acknowledgement only"])
    for review in reviews:
        lines.append(f"- {review['acknowledged_at']} · {review['review_kind']} · note: {review['note']}")
    lines.extend(["", "No signature, legal approval, official emergency designation, dispatch or infrastructure command is issued."])
    result["markdown"] = "\n".join(lines)
    return result
