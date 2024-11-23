import tkinter as tk
from typing import Callable
from ..config.constants import (
    FONT_SIZES,
    LAYOUT,
    LABEL_TEXTS,
    STYLES,
    BARCODE
)

class BarcodeEntryGroup:
    def __init__(
        self, 
        root: tk.Tk, 
        scan_callback: Callable,
        auto_tab_callback: Callable
    ):
        self.root = root
        self.scan_callback = scan_callback
        self.entries = {}
        self.variables = {}
        
        # 바코드 입력 필드 생성
        for i in range(1, 5):
            barcode_key = f"barcode{i}"
            
            # 변수 생성
            self.variables[barcode_key] = tk.StringVar()
            self.variables[barcode_key].trace("w", self.scan_callback)
            
            # 라벨 생성
            label = tk.Label(
                root,
                text=LABEL_TEXTS[barcode_key.upper()],
                font=FONT_SIZES["LARGE"]
            )
            label.place(**LAYOUT["LABELS"][barcode_key.upper()])
            
            # 입력 필드 생성
            entry = tk.Entry(
                root,
                textvariable=self.variables[barcode_key],
                font=FONT_SIZES["LARGE"]
            )
            entry.place(**LAYOUT["ENTRIES"][barcode_key.upper()])
            self.entries[barcode_key] = entry
            
            # 마지막 바코드가 아닌 경우 auto_tab 바인딩
            if i < 4:
                next_key = f"barcode{i+1}"
                entry.bind(
                    "<KeyRelease>",
                    lambda e, next_entry=next_key: self._handle_auto_tab(e, next_entry)
                )
    
    def _handle_auto_tab(self, event, next_key: str):
        """자동 탭 처리"""
        if len(event.widget.get()) == BARCODE["LENGTH"]:
            self.entries[next_key].focus_set()
    
    def get_values(self):
        """모든 바코드 값 반환"""
        return {key: var.get() for key, var in self.variables.items()}
    
    def clear_entries(self):
        """모든 바코드 입력 필드 초기화"""
        for var in self.variables.values():
            var.set("")
        self.entries["barcode1"].focus_set()
    
    def set_state(self, state: str):
        """모든 입력 필드 상태 설정"""
        for entry in self.entries.values():
            entry.configure(state=state)
    
    def set_background(self, color: str):
        """모든 입력 필드 배경색 설정"""
        for entry in self.entries.values():
            entry.configure(bg=color)
    
    def highlight_invalid(self, invalid_barcodes: list):
        """잘못된 바코드 입력 필드 하이라이트"""
        for barcode in invalid_barcodes:
            self.entries[barcode].configure(bg="red")
        self.entries["barcode1"].focus_set() 