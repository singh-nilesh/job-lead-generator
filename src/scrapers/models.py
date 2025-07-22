from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class JobDetails:
    title: str = None
    company: str = None
    location: str = None
    start_date: str = None
    duration: str = None
    stipend: str = None
    apply_by: str = None
    responsibilities: str = None
    skills_required: str = None
    other_requirements: str = None
    perks: str = None
    openings: str = None
    company_description: str = None
    posted_date: str = None
    company_url: str = None
    url: str = None
