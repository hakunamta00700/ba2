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
BARCODE_LENGTH = 10
BARCODE_PREFIXES = {
    f"{tray.id}_{uc.id}": uc.barcodePrefix 
    for tray in config.trays 
    for uc in config.ucs 
    if uc.id in tray.allowedUCs
}

# 파일 관련 상수
FILE_PATHS = {
    f"{tray.id}_{uc.id}": f"barcodes_{tray.id}_{uc.id}.txt"
    for tray in config.trays
    for uc in config.ucs
    if uc.id in tray.allowedUCs
}

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
    "TRAY1_UC1_WRONG": "You have scanned a barcode that is not TRAY 1 UC-1!!. STOP! Check labels on part Alert supervisor and quality department!",
    "TRAY1_UC2_WRONG": "You have scanned a barcode that is not TRAY 1 UC-2!!. STOP! Check labels on part Alert supervisor and quality department!",
    "TRAY2_UC1_WRONG": "Wrong barcodes scanned. You have scanned barcodes that are not tray 2 UC-1!! STOP! Check labels on part Alert supervisor and quality department!",
    "TRAY2_UC2_WRONG": "Wrong barcode scanned. You have scanned a barcode that is not tray 2 UC-2!! STOP! Check labels on part Alert supervisor and quality department!",
    "TRAY2_LABEL": "You have scanned a Tray 2 Tennessee label!! DO NOT PASS PART! STOP! Check labels on part Alert supervisor and quality department!",
    "NO_BARCODE": "No barcode has been successfully scanned.",
    "BARCODE_CLEARED": "Last scanned barcode cleared.",
    "TRAY1_UC3_WRONG": "You have scanned a barcode that is not TRAY 1 UC-3!!. STOP! Check labels on part Alert supervisor and quality department!",
    "TRAY1_UC4_WRONG": "You have scanned a barcode that is not TRAY 1 UC-4!!. STOP! Check labels on part Alert supervisor and quality department!",
    "TRAY2_UC3_WRONG": "Wrong barcodes scanned. You have scanned barcodes that are not tray 2 UC-3!! STOP! Check labels on part Alert supervisor and quality department!",
    "TRAY2_UC4_WRONG": "Wrong barcode scanned. You have scanned a barcode that is not tray 2 UC-4!! STOP! Check labels on part Alert supervisor and quality department!"
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
        "CLEAR_LAST_SCANNED": {"x": 355, "y": 195},
        "TRAY1": {"x": 1300, "y": 242},
        "TRAY2": {"x": 1300, "y": 310},
        "UC1": {"x": 1300, "y": 380},
        "UC2": {"x": 1300, "y": 450},
        "UC3": {"x": 1600, "y": 380},
        "UC4": {"x": 1600, "y": 450},
        "CLOSE": {"x": 100, "y": 300},
        "LOG_OFF": {"x": 100, "y": 250},
        "CLEAR_BARCODES": {"x": 550, "y": 850},
        "DISABLE_ALL": {"x": 100, "y": 195},
        "ENABLE_SCANNER": {"x": 550, "y": 800},
        "ENABLE_SHIFT": {"x": 742, "y": 25},
        "THIRD_SHIFT": {"x": 400, "y": 140},
        "SECOND_SHIFT": {"x": 230, "y": 140},
        "FIRST_SHIFT": {"x": 100, "y": 140},
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

# 바코드 관련 상수 (기존 드에 추가)
BARCODE = {
    "LENGTH": 10,
    "MIN_SERIES_NUMBER": 64000  # 바코드 시리즈 번호 최소값
}

# 메시지 상수 추가
SYSTEM_MESSAGES = {
    "SELECT_TRAY": "PLEASE SELECT A TRAY BEFORE SCANNING BARCODES.",
    "INTERNET_ERROR": "Internet connection issue. Saving data locally.",
    "SYNC_ERROR": "Failed to sync data: {}",
    "REMINDER_TITLE": "Reminder",
    "REMINDER_MESSAGE": "Please select UC-1, UC-2, UC-3 or UC-4 before trying to scan barcodes."
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
    "THIRD_SHIFT": "Third Shift",
    "SECOND_SHIFT": "Second Shift",
    "FIRST_SHIFT": "First Shift",
    "OPEN_COUNTER": "Open parts counter",
    "TRAY1": "TRAY 1",
    "TRAY2": "TRAY 2",
    "UC1": "UC-1",
    "UC2": "UC-2",
    "UC3": "UC-3",
    "UC4": "UC-4"
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

# 시프트 값 상수
SHIFT_VALUES = {
    "FIRST": "First Shift",
    "SECOND": "Second Shift",
    "THIRD": "Third Shift"
}

# 트레이 값 상수
TRAY_VALUES = {
    "TRAY1": "TRAY 1",
    "TRAY2": "TRAY 2"
}

# UC 값 상수
UC_VALUES = {
    "UC1": "UC-1",
    "UC2": "UC-2",
    "UC3": "UC-3",
    "UC4": "UC-4"
}

# 날짜/시간 포맷 상수
DATE_FORMATS = {
    "LOG_TIME": "%d %B %H:%M",
    "DATETIME": "%Y-%m-%d %H:%M:%S"
} 