import unittest
from unittest.mock import mock_open, patch
import os

class TestFileOperations(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            'name': 'Test User',
            'shift': '1',
            'barcode1': 'HKAD12345',
            'barcode2': 'HKAD12345',
            'barcode3': 'HKAD12345',
            'barcode4': 'HKAD12345'
        }

    @patch('builtins.open', new_callable=mock_open)
    def test_save_data_locally(self, mock_file):
        """로컬 데이터 저장 테스트"""
        save_data_locally(self.test_data)
        mock_file.assert_called_once_with('local_data.txt', 'a')
        mock_file().write.assert_called()

    def test_clear_last_scanned_barcode(self):
        """마지막 스캔 바코드 삭제 테스트"""
        global barcode_scanned_successfully
        barcode_scanned_successfully = True
        
        with patch('builtins.open', mock_open(read_data="Test barcode\n")) as mock_file:
            clear_last_scanned_barcode()
            mock_file().writelines.assert_called()
            self.assertFalse(barcode_scanned_successfully)

    def test_load_files(self):
        """파일 로드 테스트"""
        test_content = "Test content\n"
        mock_files = {
            "scan_log.txt": test_content,
            "barcodes_unknown.txt": test_content,
            "barcodes_TRAY1_UC1.txt": test_content
        }
        
        with patch('builtins.open', mock_open(read_data=test_content)):
            result = load_files()
            self.assertEqual(result["scan_log.txt"], [test_content]) 