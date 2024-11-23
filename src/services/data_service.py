import datetime
import json
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
import socket

from ..config.constants import (
    API_CONFIG,
    FILE_PATHS,
    SYSTEM_MESSAGES,
    DATE_FORMATS
)
from ..config.settings import settings

class DataService:
    def __init__(self):
        self.url = f"{settings.API_HOST}/includes/insert_barcode_injection.php"

    def save_data_locally(self, data):
        """로컬에 데이터 저장"""
        with open(FILE_PATHS["LOCAL_DATA"], 'a') as file:
            file.write(str(data) + '\n')

    def send_data_to_server(self, name, shift, barcode1, barcode2, barcode3, barcode4):
        """서버에 데이터 전송"""
        data = {
            'name': name,
            'shift': shift,
            'date_time': datetime.datetime.now().strftime(DATE_FORMATS["DATETIME"]),
            'barcode1': barcode1,
            'barcode2': barcode2,
            'barcode3': barcode3,
            'barcode4': barcode4
        }
        try:
            response = requests.post(self.url, data=data, timeout=API_CONFIG["TIMEOUT"])
            print(response.text)
        except (ConnectionError, Timeout, RequestException, socket.gaierror):
            print(SYSTEM_MESSAGES["INTERNET_ERROR"])
            self.save_data_locally(data)

    def is_internet_available(self):
        """인터넷 연결 확인"""
        try:
            requests.get('https://www.google.com/', timeout=API_CONFIG["TIMEOUT"])
            return True
        except (ConnectionError, Timeout, RequestException):
            return False

    def sync_data(self):
        """로컬 데이터를 서버와 동기화"""
        if not self.is_internet_available():
            print(SYSTEM_MESSAGES["INTERNET_ERROR"])
            return

        with open(FILE_PATHS["LOCAL_DATA"], 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            file.truncate()

            data_entries = []
            for line in lines:
                try:
                    data_entry = eval(line.strip())
                    data_entry['date_time'] = datetime.datetime.strptime(
                        data_entry['date_time'], 
                        DATE_FORMATS["DATETIME"]
                    )
                    data_entries.append(data_entry)
                except Exception as e:
                    print(SYSTEM_MESSAGES["SYNC_ERROR"].format(e))

            data_entries.sort(key=lambda x: x['date_time'])

            for data in data_entries:
                try:
                    data['date_time'] = data['date_time'].strftime(DATE_FORMATS["DATETIME"])
                    response = requests.post(self.url, data=data, timeout=API_CONFIG["TIMEOUT"])
                    print(response.text)
                except (ConnectionError, Timeout, RequestException, socket.gaierror) as e:
                    print(SYSTEM_MESSAGES["SYNC_ERROR"].format(e))
                    file.write(json.dumps(data) + '\n')

    def load_files(self):
        """필요한 파일들을 로드"""
        files_content = {}
        files_to_check = [
            FILE_PATHS["SCAN_LOG"],
            FILE_PATHS["UNKNOWN"],
            FILE_PATHS["TRAY1_UC1"],
            FILE_PATHS["TRAY1_UC2"],
            FILE_PATHS["TRAY2_UC1"],
            FILE_PATHS["TRAY2_UC2"],
        ]
        for file_name in files_to_check:
            with open(file_name, "r") as f:
                files_content[file_name] = f.readlines()
        return files_content 