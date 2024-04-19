from unittest.mock import patch
from app.config import TCXConfig, AppConfig
from unittest.mock import Mock, patch
import pytest


@pytest.fixture
def my_TCXConfig():
    with patch.object(TCXConfig, 'read', return_value=Mock()):
        yield TCXConfig()


class TestTCXConfig:

    def test_init_reads_configs(self, my_TCXConfig):
        my_TCXConfig.read.assert_called_once()
        my_TCXConfig.read.assert_called_once_with(
            [my_TCXConfig.defaults_config_file_path, my_TCXConfig.config_file_path])

    def test_get_server_url(self, my_TCXConfig):
        my_TCXConfig["3cx"] = {"scheme": "http",
                               "domain": "example.com", "port": "8080"}
        expected_url = "http://example.com:8080"
        assert my_TCXConfig.get_server_url() == expected_url

    @patch('app.config.os')
    def test_config_file_path(self, os, my_TCXConfig):
        os.getcwd.return_value = 'C:\test_dir'
        my_TCXConfig.config_file_path()
        os.path.join.assert_called_once_with(
            'C:\test_dir', 'conf', '3cx_conf.ini')

    @patch('app.config.os')
    def test_defaults_config_file_path(self, os, my_TCXConfig):
        os.getcwd.return_value = 'C:\test_dir'
        my_TCXConfig.defaults_config_file_path()
        os.path.join.assert_called_once_with(
            'C:\test_dir', 'conf', '3cx_defaults.ini')


@pytest.fixture
def my_AppConfig():
    yield AppConfig()


class TestAppConfig:
    @patch('app.config.os')
    def test_config_file_path(self, os, my_AppConfig):
        os.getcwd.return_value = 'C:\test_dir'
        my_AppConfig.config_file_path()
        os.path.join.assert_called_once_with(
            'C:\test_dir', 'conf', 'app_conf.ini')

    @patch('app.config.os')
    def test_defaults_config_file_path(self, os, my_AppConfig):
        os.getcwd.return_value = 'C:\test_dir'
        my_AppConfig.defaults_config_file_path()
        os.path.join.assert_called_once_with(
            'C:\test_dir', 'conf', 'defaults.ini')
