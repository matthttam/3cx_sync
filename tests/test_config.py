import unittest.mock
from app.config import TCXConfig, AppConfig
from unittest.mock import MagicMock, patch, PropertyMock
import pytest


@pytest.fixture
def tcx_config():
    yield TCXConfig()


class TestTCXConfig:
    # with patch.object(TCXConfig, 'read', return_value=Mock()):
    @patch('app.config.TCXConfig.read')
    def test_load(self, mock_read, tcx_config):
        tcx_config.load()
        mock_read.assert_called_once_with(
            [tcx_config.defaults_config_file_path, tcx_config.config_file_path])

    @patch.object(TCXConfig, 'config_file_path', return_value='test', new_callable=PropertyMock)
    # @patch('app.config.TCXConfig.config_file_path', return_value='test', new_callable=PropertyMock)
    @patch('builtins.open', return_value=MagicMock())
    @patch('app.config.TCXConfig.write')
    def test_save(self, mock_write, mock_open, mock_config_file_path, tcx_config):
        tcx_config.save()
        mock_file = mock_open.return_value.__enter__()
        mock_open.assert_called_once_with(
            mock_config_file_path.return_value, 'w')
        mock_write.assert_called_once_with(mock_file)
        mock_file.close.assert_called_once_with()

    def test_server_url(self, tcx_config):
        tcx_config["3cx"] = {"scheme": "http",
                             "domain": "example.com", "port": "8080"}
        expected_url = "http://example.com:8080"
        assert tcx_config.server_url == expected_url

    @patch('app.config.os.getcwd', return_value='/test')
    def test_config_file_path(self, os_getcwd, tcx_config):
        assert tcx_config.config_file_path == '/test/conf/3cx_conf.ini'
        os_getcwd.assert_called_once_with()

    @patch('app.config.os.getcwd', return_value='/test')
    def test_defaults_config_file_path(self, os_getcwd, tcx_config):
        assert tcx_config.defaults_config_file_path == '/test/conf/3cx_defaults.ini'
        os_getcwd.assert_called_once_with()


@pytest.fixture
def app_config():
    yield AppConfig()


class TestAppConfig:

    @patch('app.config.os.getcwd', return_value='/test')
    def test_config_file_path(self, os_getcwd, app_config):
        assert app_config.config_file_path == '/test/conf/app_conf.ini'
        os_getcwd.assert_called_once_with()

    @patch('app.config.os.getcwd', return_value='/test')
    def test_defaults_config_file_path(self, os_getcwd, app_config):
        assert app_config.defaults_config_file_path == '/test/conf/defaults.ini'
        os_getcwd.assert_called_once_with()
