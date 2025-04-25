from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class Content(BaseModel):
    summary: Optional[str]
    key_takeaways: Optional[List[str]]
    origin_method: Optional[str]
    source_systems: Optional[List[str]]
    supporting_evidence: Optional[List[str]]

class Confidence(BaseModel):
    level: Optional[str]
    score: Optional[float]
    validation_method: Optional[str]
    validation_date: Optional[datetime]
    linked_outcome: Optional[str]

class Fidelity(BaseModel):
    level: Optional[str]
    match_score: Optional[float]
    verified_by: Optional[List[str]]
    validated_on: Optional[datetime]
    review_needed: Optional[bool]

class Prompt(BaseModel):
    prompt_tags: Optional[List[str]]
    suggested_prompt_formats: Optional[List[str]]
    grounding_phrases: Optional[List[str]]
    copilot_priority: Optional[str]

class Reuse(BaseModel):
    times_referenced: Optional[int]
    last_used_in: Optional[str]
    linked_insights: Optional[List[str]]
    created_by: Optional[str]
    created_at: Optional[datetime]
    last_updated_by: Optional[str]
    expiration_date: Optional[datetime]

class Testing(BaseModel):
    test_recommended: Optional[bool]
    suggested_test_plan: Optional[str]
    test_priority_score: Optional[int]
    validation_status: Optional[str]

class GovernanceFeedback(BaseModel):
    user: str
    comment: str
    rating: Optional[int]
    timestamp: datetime

class Governance(BaseModel):
    governance_tags: Optional[List[str]]
    feedback_log: Optional[List[GovernanceFeedback]]

class Conflict(BaseModel):
    conflict_score: Optional[float]
    conflict_detected: Optional[bool]
    conflict_type: Optional[str]
    conflicting_with: Optional[List[str]]
    resolution_status: Optional[str]
    resolution_notes: Optional[str]
    last_conflict_check: Optional[datetime]

class NarrativeReference(BaseModel):
    type: Optional[str]
    title: Optional[str]
    url: Optional[str]
    path: Optional[str]
    label: Optional[str]
    query: Optional[str]

class Narrative(BaseModel):
    who: Optional[str]
    what: Optional[str]
    when: Optional[str]
    why: Optional[str]
    how: Optional[str]
    outcome: Optional[str]
    source: Optional[str]
    references: Optional[List[NarrativeReference]]
    watch_sources: Optional[List[NarrativeReference]]
    confidentiality: Optional[str]
    roles: Optional[List[str]]
    badge: Optional[str]
    review_status: Optional[str]

class AccessControl(BaseModel):
    visibility: Optional[str]
    allowed_roles: Optional[List[str]]
    edit_permissions: Optional[List[str]]
    view_log: Optional[List[Dict[str, str]]]

class AuditTrail(BaseModel):
    last_viewed_by: Optional[str]
    last_viewed_at: Optional[datetime]
    edit_history: Optional[List[Dict[str, str]]]

class BusinessContext(BaseModel):
    division: Optional[str]
    region: Optional[str]

class InsightUnit(BaseModel):
    schema_version: str
    id: str
    title: str
    type: str
    status: str
    tags: List[str]
    content: Optional[Content]
    confidence: Optional[Confidence]
    fidelity: Optional[Fidelity]
    prompt: Optional[Prompt]
    reuse: Optional[Reuse]
    testing: Optional[Testing]
    governance: Optional[Governance]
    conflict: Optional[Conflict]
    audience_profiles: Optional[List[str]]
    onboarding_relevance: Optional[int]
    business_context: Optional[BusinessContext]
    linked_metrics: Optional[List[str]]
    narrative: Optional[Narrative]
    access_control: Optional[AccessControl]
    audit_trail: Optional[AuditTrail]
    security_classification: Optional[str]
    confidentiality: Optional[str]
