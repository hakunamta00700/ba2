import pytest
import tkinter as tk
from unittest.mock import Mock, patch
from ui.components.barcode_entry import BarcodeEntryGroup
from ui.components.buttons import ButtonGroup
from ui.components.labels import ResultLabel, LastBarcodeLabel, UserInfoLabels
from config.constants import (
    FONT_SIZES,
    COLORS,
    ERROR_MESSAGES,
    BUTTON_TEXTS,
    LABEL_TEXTS,
    TRAY_VALUES,
    UC_VALUES,
    SHIFT_VALUES
)

@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()

class TestBarcodeEntry:
    def test_barcode_entry_creation(self, root):
        scan_callback = Mock()
        auto_tab_callback = Mock()
        
        barcode_group = BarcodeEntryGroup(root, scan_callback, auto_tab_callback)
        
        # 4개의 바코드 입력 필드가 생성되었는지 확인
        assert len(barcode_group.entries) == 4
        assert len(barcode_group.variables) == 4
        
        # 각 입력 필드의 상태 확인
        for entry in barcode_group.entries.values():
            assert isinstance(entry, tk.Entry)
            assert entry['font'] == FONT_SIZES["LARGE"]

    def test_barcode_entry_clear(self, root):
        barcode_group = BarcodeEntryGroup(root, Mock(), Mock())
        
        # 테스트 값 설정
        for var in barcode_group.variables.values():
            var.set("TEST123456")
            
        # clear_entries 호출
        barcode_group.clear_entries()
        
        # 모든 값이 지워졌는지 확인
        for var in barcode_group.variables.values():
            assert var.get() == ""

    def test_barcode_entry_state(self, root):
        barcode_group = BarcodeEntryGroup(root, Mock(), Mock())
        
        # disabled 상태 테스트
        barcode_group.set_state("disabled")
        for entry in barcode_group.entries.values():
            assert entry['state'] == 'disabled'
            
        # normal 상태 테스트
        barcode_group.set_state("normal")
        for entry in barcode_group.entries.values():
            assert entry['state'] == 'normal'

class TestButtons:
    def test_button_creation(self, root):
        callbacks = {
            "clear_last": Mock(),
            "close": Mock(),
            "log_off": Mock(),
            "clear_barcodes": Mock(),
            "disable_all": Mock(),
            "enable_scanner": Mock(),
            "enable_shift": Mock(),
            "open_counter": Mock(),
            "tray_selected": Mock(),
            "focus_barcode1": Mock()
        }
        
        button_group = ButtonGroup(
            root,
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar(),
            callbacks
        )
        
        # 버튼들이 올바르게 생성되었는지 확인
        assert isinstance(button_group.clear_last_button, tk.Button)
        assert button_group.clear_last_button['text'] == BUTTON_TEXTS["CLEAR_LAST"]
        assert button_group.clear_last_button['font'] == FONT_SIZES["MEDIUM"]

    def test_uc_button_state(self, root):
        button_group = ButtonGroup(
            root,
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar(),
            {"tray_selected": Mock()}
        )
        
        # 초기 상태 확인
        assert button_group.uc1_button['state'] == 'disabled'
        assert button_group.uc2_button['state'] == 'disabled'
        
        # 활성화 테스트
        button_group.enable_uc_buttons()
        assert button_group.uc1_button['state'] == 'normal'
        assert button_group.uc2_button['state'] == 'normal'
        
        # 비활성화 테스트
        button_group.disable_uc_buttons()
        assert button_group.uc1_button['state'] == 'disabled'
        assert button_group.uc2_button['state'] == 'disabled'

class TestLabels:
    def test_result_label(self, root):
        result_label = ResultLabel(root)
        
        # PASS 표시 테스트
        result_label.show_pass()
        assert result_label.label['text'] == "PASS"
        assert result_label.label['bg'] == COLORS["SUCCESS_BG"]
        
        # 에러 메시지 표시 테스트
        error_msg = "Test Error"
        result_label.show_error(error_msg)
        assert result_label.label['text'] == error_msg
        assert result_label.label['bg'] == COLORS["ERROR_BG"]
        
        # 초기화 테스트
        result_label.clear()
        assert result_label.label['text'] == ""
        assert result_label.label['bg'] == COLORS["DEFAULT_BG"]

    def test_last_barcode_label(self, root):
        last_barcode_label = LastBarcodeLabel(root)
        
        # 라벨 텍스트 확인
        assert last_barcode_label.label['text'] == LABEL_TEXTS["LAST_BARCODE"]
        
        # 값 설정 테스트
        test_value = "TEST123456"
        last_barcode_label.set_value(test_value)
        assert last_barcode_label.value_label['text'] == test_value 