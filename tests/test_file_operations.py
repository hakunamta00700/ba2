import pytest
import os
from unittest.mock import patch, mock_open
from services.data_service import DataService
from config.constants import FILE_PATHS

@pytest.fixture
def data_service():
    return DataService()

class TestFileOperations:
    def test_load_files(self, data_service, tmp_path):
        # 테스트용 임시 파일들 생성
        test_files = {
            "SCAN_LOG": "test scan log\n",
            "UNKNOWN": "test unknown\n",
            "TRAY1_UC1": "test tray1 uc1\n",
            "TRAY1_UC2": "test tray1 uc2\n",
            "TRAY1_UC3": "test tray1 uc3\n",
            "TRAY1_UC4": "test tray1 uc4\n",
            "TRAY2_UC1": "test tray2 uc1\n",
            "TRAY2_UC2": "test tray2 uc2\n",
            "TRAY2_UC3": "test tray2 uc3\n",
            "TRAY2_UC4": "test tray2 uc4\n"
        }
        
        # 임시 파일들 생성
        test_file_paths = {}
        for key, content in test_files.items():
            test_file = tmp_path / f"test_{key}.txt"
            test_file.write_text(content)
            test_file_paths[key] = str(test_file)
        
        # FILE_PATHS를 임시 경로로 패치
        with patch('services.data_service.FILE_PATHS', test_file_paths):
            files_content = data_service.load_files()
            
            # 각 파일의 내용 확인
            for key in test_files.keys():
                assert files_content[test_file_paths[key]] == [test_files[key]]

    @patch('builtins.open', new_callable=mock_open)
    def test_file_write_operations(self, mock_file, data_service):
        test_data = "test data\n"
        
        # 로컬 데이터 저장 테스트
        data_service.save_data_locally(test_data)
        mock_file.assert_called_with(FILE_PATHS["LOCAL_DATA"], 'a')
        mock_file().write.assert_called_with(str(test_data) + '\n')

    def test_file_existence(self):
        """필요한 파일들이 모두 존재하는지 확인"""
        required_files = [
            FILE_PATHS["SCAN_LOG"],
            FILE_PATHS["UNKNOWN"],
            FILE_PATHS["TRAY1_UC1"],
            FILE_PATHS["TRAY1_UC2"],
            FILE_PATHS["TRAY1_UC3"],
            FILE_PATHS["TRAY1_UC4"],
            FILE_PATHS["TRAY2_UC1"],
            FILE_PATHS["TRAY2_UC2"],
            FILE_PATHS["TRAY2_UC3"],
            FILE_PATHS["TRAY2_UC4"],
            FILE_PATHS["LOCAL_DATA"]
        ]
        
        for file_path in required_files:
            assert os.path.exists(file_path), f"Required file {file_path} does not exist" 