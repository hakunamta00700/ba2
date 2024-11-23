import unittest
from unittest.mock import Mock, patch
from datetime import datetime

class TestBarcodeValidation(unittest.TestCase):
    def setUp(self):
        """각 테스트 케이스 실행 전 설정"""
        self.valid_tray1_uc1 = ["HKAD12345", "HKAD12345", "HKAD12345", "HKAD12345"]
        self.valid_tray1_uc2 = ["TKAD12345", "TKAD12345", "TKAD12345", "TKAD12345"]
        self.valid_tray2_uc1 = ["HKAE12345", "HKAE12345", "HKAE12345", "HKAE12345"]
        self.valid_tray2_uc2 = ["TKAE12345", "TKAE12345", "TKAE12345", "TKAE12345"]

    def test_tray1_uc1_validation(self):
        """TRAY 1 UC-1 바코드 검증 테스트"""
        # 올바른 케이스
        result = process_tray1_uc1(*self.valid_tray1_uc1)
        self.assertEqual(result, [])  # 에러 메시지가 없어야 함

        # 잘못된 접두사
        invalid_prefix = ["TKAD12345", "HKAD12345", "HKAD12345", "HKAD12345"]
        result = process_tray1_uc1(*invalid_prefix)
        self.assertTrue(any("not TRAY 1 UC-1" in msg for msg in result))

        # 일치하지 않는 바코드
        non_matching = ["HKAD12345", "HKAD12346", "HKAD12345", "HKAD12345"]
        result = process_tray1_uc1(*non_matching)
        self.assertTrue(any("not the same as the first one" in msg for msg in result)) 

    def test_tray1_uc2_validation(self):
        """TRAY 1 UC-2 바코드 검증 테스트"""
        result = process_tray1_uc2(*self.valid_tray1_uc2)
        self.assertEqual(result, [])

        # 잘못된 접두사
        invalid_prefix = ["HKAD12345", "TKAD12345", "TKAD12345", "TKAD12345"]
        result = process_tray1_uc2(*invalid_prefix)
        self.assertTrue(any("not TRAY 1 UC-2" in msg for msg in result))

    def test_tray2_uc1_validation(self):
        """TRAY 2 UC-1 바코드 검증 테스트"""
        result = process_tray2_uc1(*self.valid_tray2_uc1)
        self.assertEqual(result, [])

        # 64000 미만 바코드 테스트
        old_series = ["HKAE63999", "HKAE63999", "HKAE63999", "HKAE63999"]
        result = process_tray2_uc1(*old_series)
        self.assertTrue(any("old series label" in msg for msg in result))

    def test_tray2_uc2_validation(self):
        """TRAY 2 UC-2 바코드 검증 테스트"""
        result = process_tray2_uc2(*self.valid_tray2_uc2)
        self.assertEqual(result, [])

    def test_duplicate_barcode_check(self):
        """중복 바코드 검사 테스트"""
        with patch('builtins.open', mock_open(read_data="Test (1): HKAD12345, HKAD12345, HKAD12345, HKAD12345\n")):
            result = process_barcodes()  # 동일한 바코드 세트로 테스트
            self.assertTrue(any("Duplicate Entry" in msg for msg in result)) 