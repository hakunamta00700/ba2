import json
from dataclasses import dataclass
from typing import List
import os
import sys
from pathlib import Path
from .default_config import DEFAULT_CONFIG

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
        # 실행 파일 디렉토리나 현재 작업 디렉토리에서 config.json 찾기
        exe_dir = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path.cwd()
        self.config_file = exe_dir / "config.json"
        
        # src 디렉토리 내의 config.json도 확인
        src_config = Path(__file__).parent.parent / "config.json"
        
        # 존재하는 config.json 파일 사용
        if self.config_file.exists():
            print(f"기존 config.json 사용: {self.config_file}")
        elif src_config.exists():
            self.config_file = src_config
            print(f"src 디렉토리의 config.json 사용: {self.config_file}")
        else:
            print(f"새로운 config.json 생성: {self.config_file}")
            
        self.load_config()
    
    def load_config(self):
        try:
            with self.config_file.open('r', encoding='utf-8') as f:
                data = json.load(f)
                self.trays = [TrayConfig(**tray) for tray in data['trays']]
                self.ucs = [UCConfig(**uc) for uc in data['ucs']]
        except FileNotFoundError:
            # 기본 설정으로 새로운 config.json 생성
            self._create_default_config()
            self.save_config()
    
    def _create_default_config(self):
        """기본 설정 생성"""
        data = DEFAULT_CONFIG
        self.trays = [TrayConfig(**tray) for tray in data['trays']]
        self.ucs = [UCConfig(**uc) for uc in data['ucs']]
    
    def save_config(self):
        data = {
            'trays': [vars(tray) for tray in self.trays],
            'ucs': [vars(uc) for uc in self.ucs]
        }
        # 디렉토리가 없으면 생성
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with self.config_file.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def add_uc(self, uc_config: UCConfig):
        self.ucs.append(uc_config)
        self.save_config()
        
    def remove_uc(self, uc_id: str):
        self.ucs = [uc for uc in self.ucs if uc.id != uc_id]
        # Update tray configurations
        for tray in self.trays:
            tray.allowedUCs = [uc for uc in tray.allowedUCs if uc != uc_id]
        self.save_config() 