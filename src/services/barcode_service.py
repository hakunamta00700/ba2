from dataclasses import dataclass
from typing import List, Tuple
from config.constants import BARCODE, BARCODE_PREFIXES, ERROR_MESSAGES, config


@dataclass
class BarcodeValidationResult:
    error_messages: List[str]
    invalid_barcodes: List[str]


class BarcodeService:
    def __init__(self):
        self.validation_mapping = {
            f"{tray.id}_{uc.id}": self._create_validator(tray.id, uc.id)
            for tray in config.trays
            for uc in config.ucs
            if uc.id in tray.allowedUCs
        }

    def _create_validator(self, tray_id: str, uc_id: str) -> callable:
        """동적으로 검증 함수 생성"""
        def validator(barcodes: List[str]) -> BarcodeValidationResult:
            error_messages = []
            invalid_barcodes = self._check_barcodes_against_first(barcodes)
            
            prefix = BARCODE_PREFIXES[f"{tray_id}_{uc_id}"]
            if not self._validate_prefix(barcodes, prefix):
                error_messages.append(
                    ERROR_MESSAGES["WRONG_TRAY"].format(f"{tray_id} {uc_id}")
                )
            elif invalid_barcodes:
                error_messages.append(ERROR_MESSAGES["MISMATCH_BARCODES"])
                
            # 시리즈 번호 검증
            if not error_messages and any(
                not self._check_series_number(barcode)
                for barcode in barcodes
                if barcode.startswith(prefix)
            ):
                error_messages.append(ERROR_MESSAGES["OLD_SERIES"])
                invalid_barcodes = ["barcode1", "barcode2", "barcode3", "barcode4"]
                
            return BarcodeValidationResult(error_messages, invalid_barcodes)
            
        return validator

    def process_barcodes(self, tray_id: str, uc_id: str, *barcodes) -> Tuple[List[str], List[str]]:
        """통합된 바코드 처리 메서드"""
        validator = self.validation_mapping.get(f"{tray_id}_{uc_id}")
        if not validator:
            return (["Invalid tray or UC combination"], [])
            
        result = validator(list(barcodes))
        return result.error_messages, result.invalid_barcodes

    def _check_barcodes_against_first(self, barcodes: List[str]) -> List[str]:
        """바코드 일치 여부 검증"""
        if not barcodes:
            return []

        first_barcode = barcodes[0]
        return [
            f"barcode{i+2}"
            for i, barcode in enumerate(barcodes[1:])
            if barcode != first_barcode
        ]

    def _validate_prefix(self, barcodes: List[str], expected_prefix: str) -> bool:
        """바코드 접두사 검증"""
        return all(barcode.startswith(expected_prefix) for barcode in barcodes)

    def _check_series_number(self, barcode: str) -> bool:
        """시리즈 번호 검증"""
        try:
            barcode_number = int(barcode[4:])
            return barcode_number >= BARCODE["MIN_SERIES_NUMBER"]
        except (ValueError, IndexError):
            return False
