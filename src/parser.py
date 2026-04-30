"""
Response parsing for structured triage output.

Confidence Mechanism:
Confidence is determined using deterministic signals from the parsed classification output:
- Whether required fields are present in the model response
- Whether the summary contains enough information to be useful
- Whether values were filled by parser defaults instead of explicit model output

This approach avoids relying only on LLM self-reported confidence, which can be unreliable.
The trade-off is that this is a conservative baseline: it may flag some valid tickets for review,
but it is safer for production triage than silently auto-classifying incomplete outputs.
"""

import re

DEFAULT_VALUES = {
    "category": "other",
    "priority": "medium",
    "assigned_team": "L1",
    "summary": "Unable to parse model response",
}

REQUIRED_FIELDS = ["category", "priority", "assigned_team", "summary"]
CONFIDENCE_THRESHOLD = 0.6


def _calculate_confidence(result, explicit_fields):
    """Calculate confidence from structural completeness and output quality."""
    confidence = 1.0

    for field in REQUIRED_FIELDS:
        if field not in explicit_fields:
            confidence -= 0.25

    if len(result.get("summary", "")) < 20:
        confidence -= 0.2

    return max(0.0, round(confidence, 2))


def parse_triage_response(raw_text):
    """Parse the model's structured response into a dict.

    Extracts FIELD: value pairs from the model's text output.
    Falls back to defaults for any missing field.
    """
    result = {}
    explicit_fields = set()

    for field in ["CATEGORY", "PRIORITY", "ASSIGNED_TEAM", "SUMMARY"]:
        key = field.lower()
        match = re.search(rf"{field}:\s*(.+)", raw_text)
        if match:
            result[key] = match.group(1).strip()
            explicit_fields.add(key)
        else:
            result[key] = DEFAULT_VALUES[key]

    confidence = _calculate_confidence(result, explicit_fields)
    result["confidence"] = confidence
    result["needs_human_review"] = confidence < CONFIDENCE_THRESHOLD

    return result