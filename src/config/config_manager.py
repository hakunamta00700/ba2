import json
from dataclasses import dataclass
from typing import List
import os

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
        self.config_file = os.path.join(os.path.dirname(__file__), "config.json")
        self.load_config()
    
    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                self.trays = [TrayConfig(**tray) for tray in data['trays']]
                self.ucs = [UCConfig(**uc) for uc in data['ucs']]
        except FileNotFoundError:
            # 기본 설정 생성
            self._create_default_config()
            self.save_config()
    
    def _create_default_config(self):
        """기본 설정 생성"""
        self.trays = [
            TrayConfig(
                id="TRAY1",
                name="TRAY 1",
                allowedUCs=["UC1", "UC2", "UC3", "UC4"]
            ),
            TrayConfig(
                id="TRAY2",
                name="TRAY 2",
                allowedUCs=["UC1", "UC2", "UC3", "UC4"]
            )
        ]
        self.ucs = [
            UCConfig(id="UC1", name="UC-1", barcodePrefix="HKAD"),
            UCConfig(id="UC2", name="UC-2", barcodePrefix="TKAD"),
            UCConfig(id="UC3", name="UC-3", barcodePrefix="LHAE"),
            UCConfig(id="UC4", name="UC-4", barcodePrefix="LHAD")
        ]
    
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