import pytest
import datetime
from unittest.mock import Mock, patch
from src.services.data_service import DataService
from src.config.constants import DATE_FORMATS

@pytest.fixture
def data_service():
    return DataService()

@pytest.fixture
def mock_response():
    mock = Mock()
    mock.text = "Success"
    return mock

class TestDataSync:
    def test_save_data_locally(self, data_service, tmp_path):
        # 임시 파일 경로 설정
        test_file = tmp_path / "test_local_data.txt"
        with patch('src.services.data_service.FILE_PATHS', {'LOCAL_DATA': str(test_file)}):
            test_data = {
                'name': 'Test User',
                'shift': 'First Shift',
                'date_time': datetime.datetime.now().strftime(DATE_FORMATS["DATETIME"]),
                'barcode1': 'HKAD65000',
                'barcode2': 'HKAD65000',
                'barcode3': 'HKAD65000',
                'barcode4': 'HKAD65000'
            }
            
            data_service.save_data_locally(test_data)
            
            # 파일이 생성되었는지 확인
            assert test_file.exists()
            # 데이터가 올바르게 저장되었는지 확인
            content = test_file.read_text()
            assert 'Test User' in content
            assert 'First Shift' in content
            assert 'HKAD65000' in content

    @patch('requests.post')
    def test_send_data_to_server_success(self, mock_post, data_service, mock_response):
        mock_post.return_value = mock_response
        
        data_service.send_data_to_server(
            'Test User',
            'First Shift',
            'HKAD65000',
            'HKAD65000',
            'HKAD65000',
            'HKAD65000'
        )
        
        # API 호출 확인
        assert mock_post.called
        # API 호출 파라미터 확인
        call_args = mock_post.call_args[1]
        assert call_args['data']['name'] == 'Test User'
        assert call_args['data']['shift'] == 'First Shift'
        assert call_args['data']['barcode1'] == 'HKAD65000'

    @patch('requests.post')
    def test_send_data_to_server_failure(self, mock_post, data_service, tmp_path):
        mock_post.side_effect = Exception("Connection error")
        test_file = tmp_path / "test_local_data.txt"
        
        with patch('src.services.data_service.FILE_PATHS', {'LOCAL_DATA': str(test_file)}):
            data_service.send_data_to_server(
                'Test User',
                'First Shift',
                'HKAD65000',
                'HKAD65000',
                'HKAD65000',
                'HKAD65000'
            )
            
            # 실패 시 로컬에 저장되었는지 확인
            assert test_file.exists()
            content = test_file.read_text()
            assert 'Test User' in content
            assert 'First Shift' in content
            assert 'HKAD65000' in content

    @patch('requests.get')
    def test_internet_availability(self, mock_get, data_service):
        # 인터넷 연결 성공 케이스
        mock_get.return_value = Mock(status_code=200)
        assert data_service.is_internet_available() is True
        
        # 인터넷 연결 실패 케이스
        mock_get.side_effect = Exception("Connection error")
        assert data_service.is_internet_available() is False 