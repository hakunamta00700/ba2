import tkinter as tk
from typing import Callable
from config.constants import (
    FONT_SIZES,
    LAYOUT,
    BUTTON_TEXTS,
    config  # ConfigManager 인스턴스 추가
)

class ButtonGroup:
    def __init__(
        self,
        root: tk.Tk,
        tray_var: tk.StringVar,
        uc_var: tk.StringVar,
        shift_var: tk.StringVar,
        callbacks: dict
    ):
        self.root = root
        self.tray_var = tray_var
        self.uc_var = uc_var
        self.shift_var = shift_var
        self.callbacks = callbacks
        
        self._create_control_buttons()
        self._create_tray_buttons()
        self._create_uc_buttons()
        self._create_shift_buttons()
    
    def _create_control_buttons(self):
        """기본 제어 버튼 생성"""
        self.clear_last_button = tk.Button(
            self.root,
            text=BUTTON_TEXTS["CLEAR_LAST"],
            font=FONT_SIZES["MEDIUM"],
            command=self.callbacks["clear_last"]
        )
        self.clear_last_button.place(**LAYOUT["BUTTONS"]["CLEAR_LAST_SCANNED"])

        self.close_button = tk.Button(
            self.root,
            text=BUTTON_TEXTS["CLOSE"],
            font=FONT_SIZES["MEDIUM"],
            command=self.callbacks["close"]
        )
        self.close_button.place(**LAYOUT["BUTTONS"]["CLOSE"])

        self.log_off_button = tk.Button(
            self.root,
            text=BUTTON_TEXTS["LOG_OFF"],
            font=FONT_SIZES["MEDIUM"],
            command=self.callbacks["log_off"]
        )
        self.log_off_button.place(**LAYOUT["BUTTONS"]["LOG_OFF"])

        # 나머지 제어 버튼들...
        self.clear_barcodes_button = tk.Button(
            self.root,
            text=BUTTON_TEXTS["CLEAR_BARCODES"],
            font=FONT_SIZES["MEDIUM"],
            command=self.callbacks["clear_barcodes"]
        )
        self.clear_barcodes_button.place(**LAYOUT["BUTTONS"]["CLEAR_BARCODES"])

        self.disable_all_button = tk.Button(
            self.root,
            text=BUTTON_TEXTS["DISABLE_ALL"],
            font=FONT_SIZES["MEDIUM"],
            command=self.callbacks["disable_all"]
        )
        self.disable_all_button.place(**LAYOUT["BUTTONS"]["DISABLE_ALL"])

        self.enable_scanner_button = tk.Button(
            self.root,
            text=BUTTON_TEXTS["ENABLE_SCANNER"],
            font=FONT_SIZES["MEDIUM"],
            command=self.callbacks["enable_scanner"]
        )
        self.enable_scanner_button.place(**LAYOUT["BUTTONS"]["ENABLE_SCANNER"])

        self.enable_shift_button = tk.Button(
            self.root,
            text=BUTTON_TEXTS["ENABLE_NAME_SHIFT"],
            font=FONT_SIZES["MEDIUM"],
            command=self.callbacks["enable_shift"]
        )
        self.enable_shift_button.place(**LAYOUT["BUTTONS"]["ENABLE_SHIFT"])

        self.count_button = tk.Button(
            self.root,
            text=BUTTON_TEXTS["OPEN_COUNTER"],
            font=FONT_SIZES["MEDIUM"],
            command=self.callbacks["open_counter"]
        )
        self.count_button.place(**LAYOUT["BUTTONS"]["COUNT"])

    def _create_tray_buttons(self):
        """트레이 선택 라디오 버튼 동적 생성"""
        self.tray_buttons = {}
        for tray in config.trays:
            self.tray_buttons[tray.id] = tk.Radiobutton(
                self.root,
                text=tray.name,
                variable=self.tray_var,
                value=tray.id,
                font=FONT_SIZES["MEDIUM"],
                command=self.callbacks["tray_selected"]
            )
            # LAYOUT에서 해당 트레이의 위치 정보 가져오기
            self.tray_buttons[tray.id].place(**LAYOUT["BUTTONS"][tray.id])

    def _create_uc_buttons(self):
        """UC 선택 라디오 버튼 동적 생성"""
        self.uc_buttons = {}
        for uc in config.ucs:
            self.uc_buttons[uc.id] = tk.Radiobutton(
                self.root,
                text=uc.name,
                variable=self.uc_var,
                value=uc.id,
                font=FONT_SIZES["MEDIUM"],
                state="disabled"
            )
            # LAYOUT에서 해당 UC의 위치 정보 가져오기
            self.uc_buttons[uc.id].place(**LAYOUT["BUTTONS"][uc.id])

    def _create_shift_buttons(self):
        """시프트 선택 버튼 생성"""
        self.first_shift_button = tk.Button(
            self.root,
            text=BUTTON_TEXTS["FIRST_SHIFT"],
            font=FONT_SIZES["MEDIUM"],
            command=lambda: self._update_shift(SHIFT_VALUES["FIRST"])
        )
        self.first_shift_button.place(**LAYOUT["BUTTONS"]["FIRST_SHIFT"])

        self.second_shift_button = tk.Button(
            self.root,
            text=BUTTON_TEXTS["SECOND_SHIFT"],
            font=FONT_SIZES["MEDIUM"],
            command=lambda: self._update_shift(SHIFT_VALUES["SECOND"])
        )
        self.second_shift_button.place(**LAYOUT["BUTTONS"]["SECOND_SHIFT"])

        self.third_shift_button = tk.Button(
            self.root,
            text=BUTTON_TEXTS["THIRD_SHIFT"],
            font=FONT_SIZES["MEDIUM"],
            command=lambda: self._update_shift(SHIFT_VALUES["THIRD"])
        )
        self.third_shift_button.place(**LAYOUT["BUTTONS"]["THIRD_SHIFT"])

    def _update_shift(self, shift_value: str):
        """시프트 값 업데이트"""
        self.shift_var.set(shift_value)
        self.callbacks["enable_scanner"]()
        self.callbacks["focus_barcode1"]()

    def enable_uc_buttons(self):
        """선택된 트레이에 허용된 UC 버튼만 활성화"""
        selected_tray = self.tray_var.get()
        tray_config = next((tray for tray in config.trays if tray.id == selected_tray), None)
        
        if tray_config:
            for uc_id, button in self.uc_buttons.items():
                if uc_id in tray_config.allowedUCs:
                    button.configure(state="normal")
                else:
                    button.configure(state="disabled")

    def disable_uc_buttons(self):
        """UC 버튼 비활성화"""
        for button in self.uc_buttons.values():
            button.configure(state="disabled")

    def deselect_all(self):
        """모든 라디오 버튼 선택 해제"""
        self.tray1_button.deselect()
        self.tray2_button.deselect()
        for button in self.uc_buttons.values():
            button.deselect() 