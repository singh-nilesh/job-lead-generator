from dataclasses import dataclass
import os

@dataclass
class Constants:
    """Class that stores various Constants."""
    
    # src dir
    src_dir = os.path.dirname(os.path.abspath(__file__))
    
    # root
    project_root = os.path.dirname(src_dir)
    
    # Artifacts dir
    artifacts_dir = os.path.join(project_root, "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True, )
    
    # Config.json
    config_path = os.path.join(src_dir, "config", "scraper_config.json")
    
    # Logs path
    logs_path = os.path.join(artifacts_dir, "logs")
    os.makedirs(logs_path, exist_ok=True)

    