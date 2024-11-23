import unittest
import tkinter as tk
from unittest.mock import Mock, patch

class TestUIComponents(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        
    def tearDown(self):
        self.root.destroy()

    def test_tray_selection(self):
        """트레이 선택 UI 테스트"""
        tray_var = tk.StringVar()
        uc_var = tk.StringVar()
        
        # TRAY 1 선택시 UC 버튼 활성화 확인
        tray_var.set("TRAY 1")
        tray_selected()
        self.assertEqual(uc1_button['state'], 'normal')
        self.assertEqual(uc2_button['state'], 'normal')

    def test_barcode_entry_validation(self):
        """바코드 입력 검증 테스트"""
        barcode_var = tk.StringVar()
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            barcode_var.set("INVALID")  # 잘못된 형식
            self.assertTrue(mock_showinfo.called) 

    def test_auto_tab_functionality(self):
        """자동 탭 기능 테스트"""
        event = Mock()
        event.widget = Mock()
        event.widget.get.return_value = "HKAD12345"  # 10자리 바코드
        next_widget = Mock()
        
        auto_tab(event, next_widget)
        self.assertTrue(next_widget.focus_set.called)

    def test_clear_functions(self):
        """초기화 기능 테스트"""
        # clear_barcode_entries 테스트
        barcode1_var = tk.StringVar(value="TEST")
        clear_barcode_entries()
        self.assertEqual(barcode1_var.get(), "")

        # clear_user_shift 테스트
        name_var = tk.StringVar(value="TEST")
        shift_var = tk.StringVar(value="1")
        clear_user_shift()
        self.assertEqual(name_var.get(), "")
        self.assertEqual(shift_var.get(), "")

    def test_shift_button_functionality(self):
        """교대 버튼 기능 테스트"""
        shift_var = tk.StringVar()
        
        update_shift1()
        self.assertEqual(shift_var.get(), "First Shift")
        
        update_shift2()
        self.assertEqual(shift_var.get(), "Second Shift")
        
        update_shift3()
        self.assertEqual(shift_var.get(), "Third Shift")