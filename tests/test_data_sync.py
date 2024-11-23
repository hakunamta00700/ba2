import unittest
from unittest.mock import Mock, patch
import requests

class TestDataSync(unittest.TestCase):
    @patch('requests.post')
    def test_send_data_to_server(self, mock_post):
        """서버 데이터 전송 테스트"""
        # 성공 케이스
        mock_post.return_value.status_code = 200
        result = send_data_to_server("Test", "1", "B1", "B2", "B3", "B4")
        self.assertTrue(mock_post.called)

        # 네트워크 오류 케이스
        mock_post.side_effect = requests.exceptions.ConnectionError
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            send_data_to_server("Test", "1", "B1", "B2", "B3", "B4")
            mock_file.assert_called_with('local_data.txt', 'a')

    def test_is_internet_available(self):
        """인터넷 연결 확인 테스트"""
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            self.assertTrue(is_internet_available())
            
            mock_get.side_effect = requests.exceptions.ConnectionError
            self.assertFalse(is_internet_available())

    def test_sync_data(self):
        """데이터 동기화 테스트"""
        test_data = '{"name": "Test", "shift": "1", "date_time": "2024-03-20 10:00:00"}\n'
        
        with patch('builtins.open', mock_open(read_data=test_data)) as mock_file:
            with patch('requests.post') as mock_post:
                mock_post.return_value.status_code = 200
                sync_data()
                self.assertTrue(mock_post.called)
                
                # 실패 케이스
                mock_post.side_effect = requests.exceptions.ConnectionError
                sync_data()
                mock_file().write.assert_called()