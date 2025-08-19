from dataclasses import dataclass, field
from typing import Optional, List, Any
from src.core.utils import load_json
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

    @classmethod
    def from_dict(cls, config_data: dict[str, Any]) -> "ScraperConfig":
        """Initialize from a dict (parsed JSON)"""
        return cls(
            job=config_data.get("job", True),
            internship=config_data.get("internship", False),
            remote=config_data.get("work_from_home", False),
            locations=config_data.get("location"),
            roles=config_data.get("role"),
            part_time=config_data.get("part_time", False),
            min_stipend=config_data.get("min_stipend", 0),
            min_salary=config_data.get("salary(lpa)", 0.0),
            timeout=config_data.get("timeout", 10),
            internshala_base_urls=config_data.get("baseUrl", {}).get("internshala", "https://internshala.com"),
            headers=config_data.get("headers", {"User-Agent": "Mozilla/5.0"}),
            experience_years=config_data.get("experience_years", 0),
        )

    @classmethod
    def load_default_cfg(cls) -> "ScraperConfig":
        """Initialize directly from JSON file"""
        config_data = load_json(Constants.config_path)
        return cls.from_dict(config_data)
