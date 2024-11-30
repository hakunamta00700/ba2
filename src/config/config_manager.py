import json
from dataclasses import dataclass
from typing import List, Optional, Tuple
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
        # PyInstaller onefile 모드를 위한 실행 파일 경로 처리
        if getattr(sys, 'frozen', False):
            # PyInstaller로 빌드된 실행 파일의 실제 위치
            base_path = Path(os.path.dirname(sys.executable))
        else:
            # 개발 환경에서는 프로젝트 루트 디렉토리 사용
            base_path = Path(__file__).parent.parent.parent
            
        self.config_file = base_path / "config.json"
        print(f"설정 파일 경로: {self.config_file}")
        self.load_config()
    
    def load_config(self):
        try:
            with self.config_file.open('r', encoding='utf-8') as f:
                data = json.load(f)
                self.trays = [TrayConfig(**tray) for tray in data['trays']]
                self.ucs = [UCConfig(**uc) for uc in data['ucs']]
        except FileNotFoundError:
            print(f"설정 파일을 찾을 수 없습니다. 기본 설정을 생성합니다: {self.config_file}")
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

    def process_barcodes(self, tray_id: str, uc_id: str, *barcodes: str) -> Tuple[List[str], List[str]]:
        # Implementation for processing barcodes
        pass 

def safe_unlink(path):
    try:
        Path(path).unlink()
    except FileNotFoundError:
        pass