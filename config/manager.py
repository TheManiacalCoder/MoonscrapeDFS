import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_path = Path(".git/config.json")
        self._load_config()
        
    def _load_config(self):
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
            
        with open(self.config_path) as f:
            config = json.load(f)
        self.email = config['email']
        self.api_key = config['api_key']
        self.openrouter_api_key = config.get('openrouter', {}).get('api_key', '')
        self.ai_model = config.get('openrouter', {}).get('ai_model', 'x-ai/grok-2-1212') 