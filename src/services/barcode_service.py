from typing import List, Tuple
from config.constants import (
    BARCODE_PREFIXES,
    ERROR_MESSAGES,
    BARCODE
)

class BarcodeService:
    @staticmethod
    def check_barcodes_against_first(
        barcode1: str, 
        barcode2: str, 
        barcode3: str, 
        barcode4: str
    ) -> List[str]:
        invalid_barcodes = []
        for barcode_name, barcode_value in [
            ("barcode2", barcode2),
            ("barcode3", barcode3),
            ("barcode4", barcode4),
        ]:
            if barcode_value != barcode1:
                invalid_barcodes.append(barcode_name)
        return invalid_barcodes

    def process_tray1_uc1(self, barcode1: str, barcode2: str, barcode3: str, barcode4: str) -> Tuple[List[str], List[str]]:
        error_messages = []
        invalid_barcodes = self.check_barcodes_against_first(
            barcode1, barcode2, barcode3, barcode4
        )
        if not all(
            barcode.startswith(BARCODE_PREFIXES["TRAY1_UC1"])
            for barcode in [barcode1, barcode2, barcode3, barcode4]
        ):
            error_messages.append(ERROR_MESSAGES["TRAY1_UC1_WRONG"])
        elif invalid_barcodes:
            error_messages.append(ERROR_MESSAGES["MISMATCH_BARCODES"])
            return error_messages, invalid_barcodes
        elif any(
            barcode.startswith(BARCODE_PREFIXES["TRAY2_UC2"])
            for barcode in [barcode1, barcode2, barcode3, barcode4]
        ):
            error_messages.append(ERROR_MESSAGES["TRAY2_LABEL"])
        else:
            for barcode in [barcode1, barcode2, barcode3, barcode4]:
                if barcode.startswith(BARCODE_PREFIXES["TRAY1_UC1"]):
                    barcode_number = int(barcode[4:])
                    if barcode_number < BARCODE["MIN_SERIES_NUMBER"]:
                        error_messages.append(ERROR_MESSAGES["OLD_SERIES"])
        return error_messages, invalid_barcodes

    def process_tray1_uc2(self, barcode1: str, barcode2: str, barcode3: str, barcode4: str) -> Tuple[List[str], List[str]]:
        error_messages = []
        invalid_barcodes = self.check_barcodes_against_first(
            barcode1, barcode2, barcode3, barcode4
        )
        if not all(
            barcode.startswith(BARCODE_PREFIXES["TRAY1_UC2"])
            for barcode in [barcode1, barcode2, barcode3, barcode4]
        ):
            error_messages.append(ERROR_MESSAGES["TRAY1_UC2_WRONG"])
        elif invalid_barcodes:
            error_messages.append(ERROR_MESSAGES["MISMATCH_BARCODES"])
        return error_messages, invalid_barcodes

    def process_tray2_uc1(self, barcode1: str, barcode2: str, barcode3: str, barcode4: str) -> Tuple[List[str], List[str]]:
        error_messages = []
        invalid_barcodes = self.check_barcodes_against_first(
            barcode1, barcode2, barcode3, barcode4
        )
        if not all(
            barcode.startswith(BARCODE_PREFIXES["TRAY2_UC1"])
            for barcode in [barcode1, barcode2, barcode3, barcode4]
        ):
            error_messages.append(ERROR_MESSAGES["TRAY2_UC1_WRONG"])
        elif invalid_barcodes:
            error_messages.append(ERROR_MESSAGES["MISMATCH_BARCODES"])
        else:
            for barcode in [barcode1, barcode2, barcode3, barcode4]:
                if barcode.startswith(BARCODE_PREFIXES["TRAY2_UC1"]):
                    barcode_number = int(barcode[4:])
                    if barcode_number < BARCODE["MIN_SERIES_NUMBER"]:
                        error_messages.append(ERROR_MESSAGES["OLD_SERIES"])
                        invalid_barcodes = ["barcode1", "barcode2", "barcode3", "barcode4"]
        return error_messages, invalid_barcodes

    def process_tray2_uc2(self, barcode1: str, barcode2: str, barcode3: str, barcode4: str) -> Tuple[List[str], List[str]]:
        error_messages = []
        invalid_barcodes = self.check_barcodes_against_first(
            barcode1, barcode2, barcode3, barcode4
        )
        if not all(
            barcode.startswith(BARCODE_PREFIXES["TRAY2_UC2"])
            for barcode in [barcode1, barcode2, barcode3, barcode4]
        ):
            error_messages.append(ERROR_MESSAGES["TRAY2_UC2_WRONG"])
        elif invalid_barcodes:
            error_messages.append(ERROR_MESSAGES["MISMATCH_BARCODES"])
        return error_messages, invalid_barcodes 