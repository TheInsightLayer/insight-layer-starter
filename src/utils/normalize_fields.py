# src/utils/normalize_fields.py

from typing import Dict

def normalize_insight(insight: Dict) -> Dict:
    """
    Normalizes legacy InsightUnit fields to the standard schema.
    This should be used before saving or validating with a schema model.
    """

    # Normalize confidence block
    if "confidence" in insight:
        confidence = insight["confidence"]
        confidence["level"] = confidence.pop("confidence_level", confidence.get("level"))
        confidence["score"] = confidence.pop("confidence_score", confidence.get("score"))
        confidence["validation_method"] = confidence.get("validation_method")
        confidence["validation_date"] = confidence.pop("date_validated", confidence.get("validation_date"))
        confidence["linked_outcome"] = confidence.get("linked_outcome")

    # Normalize fidelity block
    if "fidelity" in insight:
        fidelity = insight["fidelity"]
        fidelity["level"] = fidelity.pop("fidelity_level", fidelity.get("level"))
        fidelity["match_score"] = fidelity.pop("source_match_score", fidelity.get("match_score"))
        fidelity["verified_by"] = fidelity.get("verified_by")
        fidelity["validated_on"] = fidelity.pop("date_validated", fidelity.get("validated_on"))
        fidelity["review_needed"] = fidelity.pop("fidelity_review_needed", fidelity.get("review_needed"))

    # Normalize narrative.rewatch_sources into narrative.watch_sources
    if "narrative" in insight:
        narrative = insight["narrative"]
        if "rewatch_sources" in narrative and "watch_sources" not in narrative:
            narrative["watch_sources"] = narrative.pop("rewatch_sources")

    # Optional: normalize top-level fields (for future proofing)
    insight["confidentiality"] = insight.get("confidentiality", "internal")

    return insight
