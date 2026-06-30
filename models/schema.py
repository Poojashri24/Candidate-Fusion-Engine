from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class CandidateProfile:
    candidate_id: Optional[str] = None
    source: Optional[str] = None
    matched_sources: list = field(default_factory=list)

    full_name: Optional[str] = None

    emails: List[str] = field(default_factory=list)

    phones: List[str] = field(default_factory=list)

    location: Dict[str, Optional[str]] = field(
        default_factory=lambda: {
            "city": None,
            "region": None,
            "country": None
        }
    )

    links: Dict[str, List[str]] = field(
        default_factory=lambda: {
            "linkedin": [],
            "github": [],
            "portfolio": [],
            "other": []
        }
    )

    headline: Optional[str] = None

    years_experience: Optional[float] = None

    skills: List[Dict] = field(default_factory=list)

    experience: List[Dict] = field(default_factory=list)

    education: List[Dict] = field(default_factory=list)

    provenance: List[Dict] = field(default_factory=list)

    overall_confidence: Optional[float] = None
    
    decision_log: list = field(default_factory=list)
    