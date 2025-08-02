from src.core.utils import load_json
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from src.constants import Constants

@dataclass
class ScraperConfig:
    """Configuration for job scrapers"""
    job: bool = True
    internship: bool = False
    remote: bool = False
    locations: Optional[List[str]] = None
    roles: Optional[List[str]] = None
    part_time: bool = False
    min_stipend: int = 0
    min_salary: float = 0
    timeout: int = 10
    internshala_base_urls: str = "https://internshala.com"
    headers: dict = field(default_factory=lambda:
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    experience_years: int = 0
    
    def __post_init__(self):
        config_data = load_json(Constants.config_path)
        
        self.job = config_data["job"]
        self.internship = config_data["internship"]
        self.remote = config_data["work_from_home"]
        self.locations = config_data["location"]
        self.roles = config_data["role"]
        self.part_time = config_data["part_time"]
        self.min_stipend = config_data["min_stipend"]
        self.min_salary = config_data["salary(lpa)"]
        self.timeout = config_data["timeout"]
        self.internshala_base_urls = config_data["baseUrl"]["internshala"]
        self.headers = config_data["headers"]
        self.experience_years = config_data["experience_years"]