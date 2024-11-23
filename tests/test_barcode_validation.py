import pytest
from services.barcode_service import BarcodeService
from config.constants import BARCODE_PREFIXES, ERROR_MESSAGES

@pytest.fixture
def barcode_service():
    return BarcodeService()

class TestBarcodeValidation:
    def test_check_barcodes_against_first(self, barcode_service):
        # 모든 바코드가 동일한 경우
        assert barcode_service.check_barcodes_against_first(
            "HKAD12345", "HKAD12345", "HKAD12345", "HKAD12345"
        ) == []

        # 일부 바코드가 다른 경우
        invalid_barcodes = barcode_service.check_barcodes_against_first(
            "HKAD12345", "HKAD12346", "HKAD12345", "HKAD12347"
        )
        assert "barcode2" in invalid_barcodes
        assert "barcode4" in invalid_barcodes

    def test_process_tray1_uc1(self, barcode_service):
        # 올바른 바코드 세트
        valid_barcodes = [f"{BARCODE_PREFIXES['TRAY1_UC1']}65000"] * 4
        error_messages, invalid_barcodes = barcode_service.process_tray1_uc1(*valid_barcodes)
        assert not error_messages
        assert not invalid_barcodes

        # 잘못된 접두사
        invalid_prefix = [f"{BARCODE_PREFIXES['TRAY1_UC2']}65000"] * 4
        error_messages, invalid_barcodes = barcode_service.process_tray1_uc1(*invalid_prefix)
        assert ERROR_MESSAGES["TRAY1_UC1_WRONG"] in error_messages

        # 오래된 시리즈 번호
        old_series = [f"{BARCODE_PREFIXES['TRAY1_UC1']}63999"] * 4
        error_messages, invalid_barcodes = barcode_service.process_tray1_uc1(*old_series)
        assert ERROR_MESSAGES["OLD_SERIES"] in error_messages

    def test_process_tray2_uc1(self, barcode_service):
        # 올바른 바코드 세트
        valid_barcodes = [f"{BARCODE_PREFIXES['TRAY2_UC1']}65000"] * 4
        error_messages, invalid_barcodes = barcode_service.process_tray2_uc1(*valid_barcodes)
        assert not error_messages
        assert not invalid_barcodes

        # 잘못된 접두사
        invalid_prefix = [f"{BARCODE_PREFIXES['TRAY2_UC2']}65000"] * 4
        error_messages, invalid_barcodes = barcode_service.process_tray2_uc1(*invalid_prefix)
        assert ERROR_MESSAGES["TRAY2_UC1_WRONG"] in error_messages

        # 오래된 시리즈 번호
        old_series = [f"{BARCODE_PREFIXES['TRAY2_UC1']}63999"] * 4
        error_messages, invalid_barcodes = barcode_service.process_tray2_uc1(*old_series)
        assert ERROR_MESSAGES["OLD_SERIES"] in error_messages

    def test_process_tray1_uc3(self, barcode_service):
        # 올바른 바코드 세트
        valid_barcodes = [f"{BARCODE_PREFIXES['TRAY1_UC3']}65000"] * 4
        error_messages, invalid_barcodes = barcode_service.process_tray1_uc3(*valid_barcodes)
        assert not error_messages
        assert not invalid_barcodes

        # 잘못된 접두사
        invalid_prefix = [f"{BARCODE_PREFIXES['TRAY1_UC2']}65000"] * 4
        error_messages, invalid_barcodes = barcode_service.process_tray1_uc3(*invalid_prefix)
        assert ERROR_MESSAGES["TRAY1_UC3_WRONG"] in error_messages

    def test_process_tray1_uc4(self, barcode_service):
        # 올바른 바코드 세트
        valid_barcodes = [f"{BARCODE_PREFIXES['TRAY1_UC4']}65000"] * 4
        error_messages, invalid_barcodes = barcode_service.process_tray1_uc4(*valid_barcodes)
        assert not error_messages
        assert not invalid_barcodes

        # 잘못된 접두사
        invalid_prefix = [f"{BARCODE_PREFIXES['TRAY1_UC2']}65000"] * 4
        error_messages, invalid_barcodes = barcode_service.process_tray1_uc4(*invalid_prefix)
        assert ERROR_MESSAGES["TRAY1_UC4_WRONG"] in error_messages 