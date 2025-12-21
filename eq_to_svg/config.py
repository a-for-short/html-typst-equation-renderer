"""Configuration management for the equation renderer."""

import os
from dataclasses import dataclass, field
from pathlib import Path
import yaml

@dataclass
class Config:
    """Configuration for equation rendering."""
    html_file: str = "main.html"
    typ_folder: str = "./assets/typ"
    svg_folder: str = "./assets/svg"
    css_file: str = field(default_factory=lambda: "")  # Optional, default empty
    text_size: int = 20
    typst_command: str = "typst"
    
    @classmethod
    def from_yaml(cls, config_path: str = "config.yaml"):
        """Load configuration from YAML file."""
        config_path = Path(config_path)
        if config_path.exists():
            with open(config_path, 'r') as f:
                data = yaml.safe_load(f)
                if data is None:
                    data = {}
                return cls(**data)
        return cls()
    
    def to_yaml(self, config_path: str = "config.yaml"):
        """Save configuration to YAML file."""
        with open(config_path, 'w') as f:
            yaml.dump(self.__dict__, f, default_flow_style=False)
    
    def ensure_dirs(self):
        """Create necessary directories."""
        Path(self.typ_folder).mkdir(parents=True, exist_ok=True)
        Path(self.svg_folder).mkdir(parents=True, exist_ok=True)
    
    def __str__(self):
        """String representation for debugging."""
        return (f"Config(html_file='{self.html_file}', "
                f"typ_folder='{self.typ_folder}', "
                f"svg_folder='{self.svg_folder}', "
                f"css_file='{self.css_file}')")