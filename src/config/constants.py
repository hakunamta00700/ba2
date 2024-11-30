from .config_manager import ConfigManager

config = ConfigManager()

# UI 관련 상수
WINDOW_CONFIG = {
    "TITLE": "Daejin barcode verification program designed by clint terry",
    "WIDTH": 2000,
    "HEIGHT": 800
}

FONT_SIZES = {
    "SMALL": ("Helvetica", 12),
    "MEDIUM": ("Helvetica", 20),
    "LARGE": ("Helvetica", 30),
    "EXTRA_LARGE": ("Helvetica", 50)
}

# 바코드 관련 상수
BARCODE = {
    "LENGTH": 10,
    "MIN_SERIES_NUMBER": 64000  # 바코드 시리즈 번호 최소값
}

# 동적으로 바코드 프리픽스 생성
BARCODE_PREFIXES = {
    f"{tray.id}_{uc.id}": uc.barcodePrefix 
    for tray in config.trays 
    for uc in config.ucs 
    if uc.id in tray.allowedUCs
}

# 동적으로 파일 경로 생성
FILE_PATHS = {
    f"{tray.id}_{uc.id}": f"barcodes_{tray.id}_{uc.id}.txt"
    for tray in config.trays
    for uc in config.ucs
    if uc.id in tray.allowedUCs
}
FILE_PATHS.update({
    "UNKNOWN": "barcodes_unknown.txt",
    "LOCAL_DATA": "local_data.txt",
    "SCAN_LOG": "scan_log.txt"
})

# API 관련 상수
API_CONFIG = {
    "BASE_URL": "http://192.168.68.124",
    "BARCODE_ENDPOINT": "/includes/insert_barcode_injection.php",
    "TIMEOUT": 5
}

# 메시지 상수
ERROR_MESSAGES = {
    "NO_LOGIN": "LOG IN WITH YOUR NAME AND SHIFT BEFORE SCANNING BARCODES.",
    "SELECT_UC": "PLEASE SELECT EITHER UC-1 OR UC-2.",
    "DUPLICATE_ENTRY": "Duplicate Entry: The scanned barcode set {} has already been scanned into the database.",
    "OLD_SERIES": "You have scanned an old series label! STOP! Check labels on part Alert supervisor and quality department!",
    "WRONG_TRAY": "Wrong barcodes scanned. You have scanned barcodes that are not {} !! STOP! Check labels on part Alert supervisor and quality department!",
    "MISMATCH_BARCODES": "Some of your barcodes are not the same as the first one! Do not pass part. Recheck your labels!",
    "NO_BARCODE": "No barcode has been successfully scanned.",
    "BARCODE_CLEARED": "Last scanned barcode cleared."
}

SYSTEM_MESSAGES = {
    "SELECT_TRAY": "PLEASE SELECT A TRAY BEFORE SCANNING BARCODES.",
    "INTERNET_ERROR": "Internet connection issue. Saving data locally.",
    "SYNC_ERROR": "Failed to sync data: {}",
    "REMINDER_TITLE": "Reminder",
    "REMINDER_MESSAGE": "Please select UC before trying to scan barcodes."
}

# 시간 관련 상수
TIMING = {
    "ERROR_DISPLAY": 10000,  # 10 seconds
    "PASS_DISPLAY": 10000,   # 10 seconds
    "DUPLICATE_DISPLAY": 15000,  # 15 seconds
    "CLEAR_RESULT": 15000,  # 15 seconds for clearing result
    "INTERNET_TIMEOUT": 3000,  # 3 seconds for internet check
    "BACKGROUND_CLEAR": 10000  # 10 seconds for clearing background
}

# UI 레이아웃 관련 상수
LAYOUT = {
    "BUTTONS": {
        # 동적으로 TRAY 버튼 위치 생성
        **{
            tray.id: {"x": 1300, "y": 242 + (i * 68)}
            for i, tray in enumerate(config.trays)
        },
        # 동적으로 UC 버튼 위치 생성
        **{
            uc.id: {"x": 1300 + (i // 2 * 300), "y": 380 + (i % 2 * 70)}
            for i, uc in enumerate(config.ucs)
        },
        "CLEAR_LAST_SCANNED": {"x": 355, "y": 195},
        "CLOSE": {"x": 100, "y": 300},
        "LOG_OFF": {"x": 100, "y": 250},
        "CLEAR_BARCODES": {"x": 550, "y": 850},
        "DISABLE_ALL": {"x": 100, "y": 195},
        "ENABLE_SCANNER": {"x": 550, "y": 800},
        "ENABLE_SHIFT": {"x": 742, "y": 25},
        "FIRST_SHIFT": {"x": 100, "y": 140},
        "SECOND_SHIFT": {"x": 230, "y": 140},
        "THIRD_SHIFT": {"x": 400, "y": 140},
        "COUNT": {"x": 546, "y": 140}
    },
    "LABELS": {
        "NAME": {"x": 100, "y": 10},
        "SHIFT": {"x": 100, "y": 70},
        "LAST_BARCODE": {"x": 100, "y": 370},
        "LAST_BARCODE_VALUE": {"x": 100, "y": 400},
        "BARCODE1": {"x": 300, "y": 450},
        "BARCODE2": {"x": 300, "y": 500},
        "BARCODE3": {"x": 300, "y": 550},
        "BARCODE4": {"x": 300, "y": 600}
    },
    "ENTRIES": {
        "NAME": {"x": 250, "y": 10},
        "SHIFT": {"x": 250, "y": 70},
        "BARCODE1": {"x": 500, "y": 450},
        "BARCODE2": {"x": 500, "y": 500},
        "BARCODE3": {"x": 500, "y": 550},
        "BARCODE4": {"x": 500, "y": 600}
    },
    "RESULT_LABEL": {
        "x": 1200,
        "y": 500,
        "width": 700,
        "height": 500
    }
}

# UI 스타일 관련 상수
STYLES = {
    "LABEL_WRAPLENGTH": 150,
    "ENTRY_JUSTIFY": "center"
}

# 색상 관련 상수
COLORS = {
    "ERROR_FG": "red",
    "ERROR_BG": "yellow",
    "SUCCESS_BG": "green",
    "DEFAULT_BG": "SystemButtonFace",
    "WHITE": "white",
    "BLACK": "black"
}

# 키 바인딩 관련 상수
KEY_BINDINGS = {
    "FULLSCREEN_EXIT": {
        "state": 4,
        "key": "e"
    },
    "QUIT": {
        "state": 4,
        "key": "q"
    },
    "ENABLE_SCANNER": "<F12>"
}

# 버튼 텍스트 상수
BUTTON_TEXTS = {
    "CLEAR_LAST": "Clear Last Scanned",
    "CLOSE": "Close",
    "LOG_OFF": "Log Off",
    "CLEAR_BARCODES": "Clear Barcodes",
    "DISABLE_ALL": "Disable ALL inputs",
    "ENABLE_SCANNER": "Enable Scanner",
    "ENABLE_NAME_SHIFT": "Enable name/shift",
    "FIRST_SHIFT": "First Shift",
    "SECOND_SHIFT": "Second Shift",
    "THIRD_SHIFT": "Third Shift",
    "OPEN_COUNTER": "Open parts counter"
}

# 라벨 텍스트 상수
LABEL_TEXTS = {
    "NAME": "Name:",
    "SHIFT": "Shift:",
    "BARCODE1": "Barcode 1:",
    "BARCODE2": "Barcode 2:",
    "BARCODE3": "Barcode 3:",
    "BARCODE4": "Barcode 4:",
    "LAST_BARCODE": "Last Scanned Barcode Set:"
}

# 날짜/시간 포맷 상수
DATE_FORMATS = {
    "LOG_TIME": "%d %B %H:%M",
    "DATETIME": "%Y-%m-%d %H:%M:%S"
}

# TRAY와 UC 값 상수 동적 생성
TRAY_VALUES = {
    tray.id: tray.name
    for tray in config.trays
}

UC_VALUES = {
    uc.id: uc.name
    for uc in config.ucs
}

# 시프트 값 상수 (기존 코드에 없었던 부분도 추가)
SHIFT_VALUES = {
    "FIRST": "First Shift",
    "SECOND": "Second Shift",
    "THIRD": "Third Shift"
} 