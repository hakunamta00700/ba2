import tkinter as tk
from typing import Callable
import subprocess
import os
import datetime

from config.constants import (
    WINDOW_CONFIG,
    KEY_BINDINGS,
    LAYOUT,
    ERROR_MESSAGES,
    COLORS,
    TRAY_VALUES,
    BARCODE,
    SYSTEM_MESSAGES,
    TIMING,
    DATE_FORMATS
)
from .components.barcode_entry import BarcodeEntryGroup
from .components.buttons import ButtonGroup
from .components.labels import ResultLabel, LastBarcodeLabel, UserInfoLabels
from ..services.barcode_service import BarcodeService
from ..services.data_service import DataService

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.barcode_service = BarcodeService()
        self.data_service = DataService()
        self._setup_window()
        self._setup_variables()
        self._setup_components()
        self._setup_bindings()
        
    def _setup_window(self):
        """윈도우 기본 설정"""
        self.root.title(WINDOW_CONFIG["TITLE"])
        window_width = WINDOW_CONFIG["WIDTH"]
        window_height = WINDOW_CONFIG["HEIGHT"]
        
        # 윈도우 위치 계산
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        self.root.attributes("-fullscreen", False)
        self.root.attributes("-topmost", True)
        self.root.after_idle(self.root.attributes, "-topmost", True)
        
    def _setup_variables(self):
        """tkinter 변수 설정"""
        self.name_var = tk.StringVar()
        self.shift_var = tk.StringVar()
        self.tray_var = tk.StringVar()
        self.uc_var = tk.StringVar()
        
        # 바코드 스캔 상태 변수
        self.scanning_in_progress = False
        self.barcode_scanned_successfully = False
        self.last_barcode_set = ""
        
    def _setup_components(self):
        """UI 컴포넌트 설정"""
        # 콜백 함수 딕셔너리 생성
        callbacks = {
            "clear_last": self.clear_last_scanned_barcode,
            "close": self.root.quit,
            "log_off": self.clear_user_shift,
            "clear_barcodes": self.clear_barcode_entries,
            "disable_all": self.disable_barcodesindef,
            "enable_scanner": self.enable_barcodes,
            "enable_shift": self.enable_nameshift,
            "open_counter": self.open_other_file,
            "tray_selected": self.tray_selected,
            "focus_barcode1": lambda: self.barcode_entries.entries["barcode1"].focus_set()
        }
        
        # 컴포넌트 초기화
        self.buttons = ButtonGroup(
            self.root,
            self.tray_var,
            self.uc_var,
            self.shift_var,
            callbacks
        )
        
        self.barcode_entries = BarcodeEntryGroup(
            self.root,
            self.scan_barcodes,
            self.auto_tab
        )
        
        self.result_label = ResultLabel(self.root)
        self.last_barcode_label = LastBarcodeLabel(self.root)
        self.user_info_labels = UserInfoLabels(self.root)
        
        # 초기 상태 설정
        self.barcode_entries.set_state("disabled")
        
    def _setup_bindings(self):
        """키 바인딩 설정"""
        self.root.bind_all("<Key>", self.handle_keys)
        self.root.bind(KEY_BINDINGS["ENABLE_SCANNER"], self.on_switch_key_press)
        
    def handle_keys(self, event):
        """키 이벤트 처리"""
        if (event.state == KEY_BINDINGS["FULLSCREEN_EXIT"]["state"] and 
            event.keysym == KEY_BINDINGS["FULLSCREEN_EXIT"]["key"]):
            self.root.attributes("-fullscreen", False)
        elif (event.state == KEY_BINDINGS["QUIT"]["state"] and 
              event.keysym == KEY_BINDINGS["QUIT"]["key"]):
            self.root.quit()
            
    def on_switch_key_press(self, event):
        """F12 키 처리"""
        self.enable_barcodes()
    
    def run(self):
        """메인 루프 실행"""
        self.root.mainloop() 

    def clear_last_scanned_barcode(self):
        """마지막 스캔된 바코드 삭제"""
        if not self.barcode_scanned_successfully:
            self.last_barcode_label.set_value(ERROR_MESSAGES["NO_BARCODE"])
            return

        tray_value = self.tray_var.get()
        uc_value = self.uc_var.get()
        filename = self.determine_filename(tray_value, uc_value)

        with open(filename, "r") as f:
            lines = f.readlines()

        if len(lines) == 0:
            return

        lines = lines[:-1]
        with open(filename, "w") as f:
            f.writelines(lines)

        self.last_barcode_label.set_value(ERROR_MESSAGES["BARCODE_CLEARED"])
        self.barcode_scanned_successfully = False

    def clear_user_shift(self, *args):
        """사용자 및 시프트 정보 초기화"""
        self.name_var.set("")
        self.shift_var.set("")
        self.barcode_entries.clear_entries()
        self.enable_nameshift()
        self.user_info_labels.name_label.focus_set()

    def clear_barcode_entries(self):
        """바코드 입력 필드 초기화"""
        self.barcode_entries.clear_entries()

    def disable_barcodesindef(self):
        """바코드 입력 비활성화"""
        self.barcode_entries.set_state("disabled")
        self.name_entry.configure(state="disabled")
        self.shift_entry.configure(state="disabled")

    def enable_barcodes(self):
        """바코드 입력 활성화"""
        self.barcode_entries.set_state("normal")
        self.barcode_entries.set_background(COLORS["WHITE"])
        self.barcode_entries.entries["barcode1"].focus_set()

    def enable_nameshift(self):
        """이름/시프트 입력 활성화"""
        self.name_entry.configure(state="normal")
        self.shift_entry.configure(state="normal")

    def tray_selected(self, *args):
        """트레이 선택 처리"""
        tray_value = self.tray_var.get()
        if tray_value in [TRAY_VALUES["TRAY1"], TRAY_VALUES["TRAY2"]]:
            self.buttons.enable_uc_buttons()
        else:
            self.buttons.disable_uc_buttons()
        self.uc_var.set("")

    def scan_barcodes(self, *args):
        """바코드 스캔 처리"""
        if self.scanning_in_progress:
            return

        name = self.name_var.get()
        shift = self.shift_var.get()
        barcodes = self.barcode_entries.get_values()

        if not name or not shift:
            self.result_label.show_error(ERROR_MESSAGES["NO_LOGIN"])
            return

        if len(barcodes["barcode4"]) == BARCODE["LENGTH"]:
            self.process_barcodes()

        tray_value = self.tray_var.get()
        uc_value = self.uc_var.get()

        if tray_value in [TRAY_VALUES["TRAY1"], TRAY_VALUES["TRAY2"]] and not uc_value:
            self.result_label.show_error(ERROR_MESSAGES["SELECT_UC"])
            return

    def process_barcodes(self, *args):
        """바코드 처리"""
        self.scanning_in_progress = True
        name = self.name_var.get()
        shift = self.shift_var.get()
        barcodes = self.barcode_entries.get_values()

        error_messages = []

        # 기본 검증
        if not self.tray_var.get():
            error_messages.append(SYSTEM_MESSAGES["SELECT_TRAY"])
            self.barcode_entries.entries["barcode1"].focus_set()

        if not name or not shift:
            error_messages.append(ERROR_MESSAGES["NO_LOGIN"])
            self.barcode_entries.entries["barcode1"].focus_set()

        # 트레이와 UC 선택에 따른 바코드 검증
        if self.tray_var.get() == TRAY_VALUES["TRAY1"]:
            if self.uc_var.get() == UC_VALUES["UC1"]:
                error_messages, invalid_barcodes = self.barcode_service.process_tray1_uc1(
                    barcodes["barcode1"], barcodes["barcode2"], 
                    barcodes["barcode3"], barcodes["barcode4"]
                )
            elif self.uc_var.get() == UC_VALUES["UC2"]:
                error_messages, invalid_barcodes = self.barcode_service.process_tray1_uc2(
                    barcodes["barcode1"], barcodes["barcode2"], 
                    barcodes["barcode3"], barcodes["barcode4"]
                )
        elif self.tray_var.get() == TRAY_VALUES["TRAY2"]:
            if self.uc_var.get() == UC_VALUES["UC1"]:
                error_messages, invalid_barcodes = self.barcode_service.process_tray2_uc1(
                    barcodes["barcode1"], barcodes["barcode2"], 
                    barcodes["barcode3"], barcodes["barcode4"]
                )
            elif self.uc_var.get() == UC_VALUES["UC2"]:
                error_messages, invalid_barcodes = self.barcode_service.process_tray2_uc2(
                    barcodes["barcode1"], barcodes["barcode2"], 
                    barcodes["barcode3"], barcodes["barcode4"]
                )

        # 에러가 없으면 바코드 배경색 초기화
        if not error_messages:
            self.barcode_entries.set_background(COLORS["WHITE"])

        # 에러 처리
        if error_messages:
            error_message = "\n".join(error_messages)
            self.result_label.show_error(error_message)
            self.barcode_entries.clear_entries()
            self.barcode_entries.entries["barcode1"].focus_set()
            
            # 타이머 설정
            self.root.after(TIMING["BACKGROUND_CLEAR"], self.barcode_entries.set_background(COLORS["WHITE"]))
            self.root.after(TIMING["ERROR_DISPLAY"], self.result_label.clear)
            
            self.scanning_in_progress = False
            self.barcode_entries.set_state("disabled")
            return

        # 바코드 세트 생성 및 중복 체크
        barcode_set = f"{barcodes['barcode1']}, {barcodes['barcode2']}, {barcodes['barcode3']}, {barcodes['barcode4']}"
        filename = self.determine_filename(self.tray_var.get(), self.uc_var.get())

        # 중복 바코드 체크
        duplicate_barcodes = False
        with open(filename, "r") as f:
            log_lines = f.readlines()
            for line in log_lines:
                if barcode_set in line:
                    duplicate_barcodes = True
                    break

        if duplicate_barcodes:
            duplicate_message = ERROR_MESSAGES["DUPLICATE_ENTRY"].format(barcode_set)
            self.barcode_entries.highlight_invalid(["barcode1", "barcode2", "barcode3", "barcode4"])
            self.result_label.show_error(duplicate_message)
            self.root.after(TIMING["DUPLICATE_DISPLAY"], self.result_label.clear)
            self.barcode_entries.clear_entries()
            self.barcode_entries.entries["barcode1"].focus_set()
            self.barcode_entries.set_state("disabled")
        else:
            # 서버에 데이터 전송
            self.data_service.send_data_to_server(
                name, shift, 
                barcodes["barcode1"], barcodes["barcode2"], 
                barcodes["barcode3"], barcodes["barcode4"]
            )

            # 로컬 파일에 저장
            with open(filename, "a") as f:
                f.write(f"{name} ({shift}): {barcode_set} {datetime.datetime.now().strftime(DATE_FORMATS['LOG_TIME'])}\n")
                self.barcode_scanned_successfully = True

            # UI 업데이트
            self.last_barcode_set = barcode_set
            self.last_barcode_label.set_value(self.last_barcode_set)
            self.barcode_entries.clear_entries()
            self.result_label.show_pass()
            self.barcode_entries.entries["barcode1"].focus_set()
            self.barcode_entries.set_state("disabled")
            self.data_service.sync_data()

        self.scanning_in_progress = False

    def open_other_file(self):
        """부품 카운터 프로그램 실행"""
        current_directory = os.path.dirname(os.path.abspath(__file__))
        target_script = os.path.join(current_directory, "parts_counter.py")
        subprocess.Popen(["python", target_script]) 