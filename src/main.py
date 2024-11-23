from src.config.constants import (
    WINDOW_CONFIG, 
    FONT_SIZES, 
    BARCODE_PREFIXES,
    FILE_PATHS, 
    API_CONFIG,
    ERROR_MESSAGES,
    TIMING,
    LAYOUT,
    STYLES,
    BARCODE,
    SYSTEM_MESSAGES,
    COLORS,
    KEY_BINDINGS,
    BUTTON_TEXTS,
    LABEL_TEXTS,
    SHIFT_VALUES,
    TRAY_VALUES,
    UC_VALUES,
    DATE_FORMATS
)
from src.config.settings import settings
from src.ui.main_window import MainWindow

def main():
    """메인 프로그램 실행"""
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main() 