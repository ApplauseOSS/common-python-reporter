"""Tests for the utils module."""

from applause.common_python_reporter.heartbeat import HeartbeatService
from unittest.mock import patch, MagicMock
import time


class TestHeartbeatService:
    """Tests for the heartbeat service."""

    def test_hearbeat(self):
        """Test the heartbeat service class."""
        with patch('applause.common_python_reporter.auto_api.AutoApi') as auto_api:
            
            mock_heartbeat_func = MagicMock()
            auto_api.send_sdk_heartbeat = mock_heartbeat_func
            heartbeat_service = HeartbeatService(auto_api, 123, sleep_time=0.1)

            print("Starting heartbeat service")
            heartbeat_service.start()
            time.sleep(0.2)
            heartbeat_service.stop()
            mock_heartbeat_func.assert_called()
            mock_heartbeat_func.assert_called_with(123)

        

        
