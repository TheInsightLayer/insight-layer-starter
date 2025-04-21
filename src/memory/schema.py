
from pydantic import BaseModel
from typing import List, Optional

class InsightLink(BaseModel):
    type: str
    insight_id: str

class InsightReference(BaseModel):
    type: str
    title: str
    url: str

class WatchSource(BaseModel):
    type: str
    query: Optional[str] = None
    path: Optional[str] = None
    url: Optional[str] = None
    label: Optional[str] = None

class InsightUnit(BaseModel):
    who: str
    what: str
    when: str
    why: str
    how: str
    outcome: str
    source: Optional[str] = None
    links: Optional[List[InsightLink]] = []
    references: Optional[List[InsightReference]] = []
    watch_sources: Optional[List[WatchSource]] = []
    roles: Optional[List[str]] = []  # New: Role relevance
    confidentiality: Optional[str] = "public"
    impact_score: Optional[float] = 5.0
    used_count: Optional[int] = 0
    linked_count: Optional[int] = 0
    outcome_match: Optional[float] = 0.5
    importance_score: Optional[float] = 0.0
    review_status: Optional[str] = "pending"
    confidence_score: Optional[float] = 0.8
    sensitivity_score: Optional[float] = 0.2
