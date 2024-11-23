from typing import List, Tuple, Callable, Optional
from dataclasses import dataclass
from config.constants import (
    BARCODE_PREFIXES,
    ERROR_MESSAGES,
    BARCODE
)

@dataclass
class BarcodeValidationResult:
    error_messages: List[str]
    invalid_barcodes: List[str]

class BarcodeService:
    def __init__(self):
        self.validation_mapping = {
            "TRAY1_UC1": self._validate_tray1_uc1,
            "TRAY1_UC2": self._validate_tray1_uc2,
            "TRAY2_UC1": self._validate_tray2_uc1,
            "TRAY2_UC2": self._validate_tray2_uc2
        }

    def _check_barcodes_against_first(
        self,
        barcodes: List[str]
    ) -> List[str]:
        """바코드 일치 여부 검증"""
        if not barcodes:
            return []
        
        first_barcode = barcodes[0]
        return [
            f"barcode{i+2}"
            for i, barcode in enumerate(barcodes[1:])
            if barcode != first_barcode
        ]

    def _validate_prefix(
        self,
        barcodes: List[str],
        expected_prefix: str
    ) -> bool:
        """바코드 접두사 검증"""
        return all(
            barcode.startswith(expected_prefix)
            for barcode in barcodes
        )

    def _check_series_number(
        self,
        barcode: str
    ) -> bool:
        """시리즈 번호 검증"""
        try:
            barcode_number = int(barcode[4:])
            return barcode_number >= BARCODE["MIN_SERIES_NUMBER"]
        except ValueError:
            return False

    def _validate_common(
        self,
        barcodes: List[str],
        prefix: str,
        error_message: str
    ) -> BarcodeValidationResult:
        """공통 검증 로직"""
        error_messages = []
        invalid_barcodes = self._check_barcodes_against_first(barcodes)

        if not self._validate_prefix(barcodes, BARCODE_PREFIXES[prefix]):
            error_messages.append(error_message)
        elif invalid_barcodes:
            error_messages.append(ERROR_MESSAGES["MISMATCH_BARCODES"])

        return BarcodeValidationResult(error_messages, invalid_barcodes)

    def _validate_tray1_uc1(
        self,
        barcodes: List[str]
    ) -> BarcodeValidationResult:
        result = self._validate_common(
            barcodes,
            "TRAY1_UC1",
            ERROR_MESSAGES["TRAY1_UC1_WRONG"]
        )

        if not result.error_messages:
            if any(
                barcode.startswith(BARCODE_PREFIXES["TRAY2_UC2"])
                for barcode in barcodes
            ):
                result.error_messages.append(ERROR_MESSAGES["TRAY2_LABEL"])
            
            if any(
                not self._check_series_number(barcode)
                for barcode in barcodes
                if barcode.startswith(BARCODE_PREFIXES["TRAY1_UC1"])
            ):
                result.error_messages.append(ERROR_MESSAGES["OLD_SERIES"])

        return result

    def _validate_tray1_uc2(
        self,
        barcodes: List[str]
    ) -> BarcodeValidationResult:
        """TRAY1_UC2 검증 로직"""
        return self._validate_common(
            barcodes,
            "TRAY1_UC2",
            ERROR_MESSAGES["TRAY1_UC2_WRONG"]
        )

    def _validate_tray2_uc1(
        self,
        barcodes: List[str]
    ) -> BarcodeValidationResult:
        """TRAY2_UC1 검증 로직"""
        result = self._validate_common(
            barcodes,
            "TRAY2_UC1",
            ERROR_MESSAGES["TRAY2_UC1_WRONG"]
        )

        if not result.error_messages:
            if any(
                not self._check_series_number(barcode)
                for barcode in barcodes
                if barcode.startswith(BARCODE_PREFIXES["TRAY2_UC1"])
            ):
                result.error_messages.append(ERROR_MESSAGES["OLD_SERIES"])
                result.invalid_barcodes = ["barcode1", "barcode2", "barcode3", "barcode4"]

        return result

    def _validate_tray2_uc2(
        self,
        barcodes: List[str]
    ) -> BarcodeValidationResult:
        """TRAY2_UC2 검증 로직"""
        return self._validate_common(
            barcodes,
            "TRAY2_UC2",
            ERROR_MESSAGES["TRAY2_UC2_WRONG"]
        )

    # 기존 public 메서드들 - 내부적으로 새로운 구현 사용
    def check_barcodes_against_first(
        self,
        barcode1: str, 
        barcode2: str, 
        barcode3: str, 
        barcode4: str
    ) -> List[str]:
        barcodes = [barcode1, barcode2, barcode3, barcode4]
        return self._check_barcodes_against_first(barcodes)

    def process_tray1_uc1(
        self,
        barcode1: str,
        barcode2: str,
        barcode3: str,
        barcode4: str
    ) -> Tuple[List[str], List[str]]:
        result = self._validate_tray1_uc1([barcode1, barcode2, barcode3, barcode4])
        return result.error_messages, result.invalid_barcodes

    def process_tray1_uc2(
        self,
        barcode1: str,
        barcode2: str,
        barcode3: str,
        barcode4: str
    ) -> Tuple[List[str], List[str]]:
        result = self._validate_tray1_uc2([barcode1, barcode2, barcode3, barcode4])
        return result.error_messages, result.invalid_barcodes

    def process_tray2_uc1(
        self,
        barcode1: str,
        barcode2: str,
        barcode3: str,
        barcode4: str
    ) -> Tuple[List[str], List[str]]:
        result = self._validate_tray2_uc1([barcode1, barcode2, barcode3, barcode4])
        return result.error_messages, result.invalid_barcodes

    def process_tray2_uc2(
        self,
        barcode1: str,
        barcode2: str,
        barcode3: str,
        barcode4: str
    ) -> Tuple[List[str], List[str]]:
        result = self._validate_tray2_uc2([barcode1, barcode2, barcode3, barcode4])
        return result.error_messages, result.invalid_barcodes