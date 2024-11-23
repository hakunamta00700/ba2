import tkinter as tk
from config.constants import (
    FONT_SIZES,
    LAYOUT,
    LABEL_TEXTS,
    STYLES,
    COLORS
)

class ResultLabel:
    def __init__(self, root: tk.Tk):
        self.label = tk.Label(
            root,
            text="",
            font=FONT_SIZES["EXTRA_LARGE"],
            width=20,
            height=5
        )
        self.label.place(**LAYOUT["RESULT_LABEL"])
    
    def show_pass(self):
        """PASS 메시지 표시"""
        self.label.config(
            text="PASS",
            font=FONT_SIZES["EXTRA_LARGE"],
            fg=COLORS["BLACK"],
            bg=COLORS["SUCCESS_BG"],
        )
    
    def show_error(self, message: str):
        """에러 메시지 표시"""
        self.label.config(
            text=message,
            font=FONT_SIZES["MEDIUM"],
            fg=COLORS["BLACK"],
            bg=COLORS["ERROR_BG"],
            wraplength=STYLES["LABEL_WRAPLENGTH"],
        )
    
    def clear(self):
        """라벨 초기화"""
        self.label.config(
            text="",
            bg=COLORS["DEFAULT_BG"]
        )


class LastBarcodeLabel:
    def __init__(self, root: tk.Tk):
        # 라벨 생성
        self.label = tk.Label(
            root,
            text=LABEL_TEXTS["LAST_BARCODE"],
            font=FONT_SIZES["SMALL"]
        )
        self.label.place(**LAYOUT["LABELS"]["LAST_BARCODE"])
        
        # 값 표시 라벨
        self.value_label = tk.Label(
            root,
            text="",
            font=FONT_SIZES["SMALL"],
            wraplength=STYLES["LABEL_WRAPLENGTH"]
        )
        self.value_label.place(**LAYOUT["LABELS"]["LAST_BARCODE_VALUE"])
    
    def set_value(self, value: str):
        """마지막 스캔 바코드 값 설정"""
        self.value_label.config(text=value)


class UserInfoLabels:
    def __init__(self, root: tk.Tk):
        # 이름 라벨
        self.name_label = tk.Label(
            root,
            text=LABEL_TEXTS["NAME"],
            font=FONT_SIZES["LARGE"]
        )
        self.name_label.place(**LAYOUT["LABELS"]["NAME"])
        
        # 시프트 라벨
        self.shift_label = tk.Label(
            root,
            text=LABEL_TEXTS["SHIFT"],
            font=FONT_SIZES["LARGE"]
        )
        self.shift_label.place(**LAYOUT["LABELS"]["SHIFT"]) 