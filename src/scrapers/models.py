from dataclasses import dataclass, field
from typing import Optional

@dataclass
class JobDetails:
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    duration: Optional[str] = None
    stipend: Optional[str] = None
    apply_by: Optional[str] = None
    responsibilities: Optional[str] = None
    skills_required: Optional[str] = None
    other_requirements: Optional[str] = None
    perks: Optional[str] = None
    openings: Optional[str] = None
    company_description: Optional[str] = None
    posted_date: Optional[str] = None
    company_url: Optional[str] = None
    url: Optional[str] = None
