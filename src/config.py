from src.utils import load_json
from dataclasses import dataclass
import os
from typing import Dict, List, Any

# Get the directory where config.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(current_dir, "config", "scraper_config.json")

@dataclass
class ScraperConfig:
    """Configuration for job scrapers"""
    job: bool = True
    internship: bool = False
    remote: bool = False
    locations: List[str] = None
    roles: List[str] = None
    part_time: bool = False
    min_stipend: int = 0
    min_salary: float = 0
    timeout: int = 10
    internshala_base_urls: str = None
    headers: Dict[str, str] = None
    experience_years: int = 0
    
    def __post_init__(self):
        config_data = load_json(config_path)
        
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