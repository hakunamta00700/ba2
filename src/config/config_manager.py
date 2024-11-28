import json
from dataclasses import dataclass
from typing import List

@dataclass
class UCConfig:
    id: str
    name: str
    barcodePrefix: str

@dataclass 
class TrayConfig:
    id: str
    name: str
    allowedUCs: List[str]

class ConfigManager:
    def __init__(self):
        self.config_file = "src/config/config.json"
        self.load_config()
    
    def load_config(self):
        with open(self.config_file, 'r') as f:
            data = json.load(f)
            self.trays = [TrayConfig(**tray) for tray in data['trays']]
            self.ucs = [UCConfig(**uc) for uc in data['ucs']]
    
    def save_config(self):
        data = {
            'trays': [vars(tray) for tray in self.trays],
            'ucs': [vars(uc) for uc in self.ucs]
        }
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=2)
            
    def add_uc(self, uc_config: UCConfig):
        self.ucs.append(uc_config)
        self.save_config()
        
    def remove_uc(self, uc_id: str):
        self.ucs = [uc for uc in self.ucs if uc.id != uc_id]
        # Update tray configurations
        for tray in self.trays:
            tray.allowedUCs = [uc for uc in tray.allowedUCs if uc != uc_id]
        self.save_config() 