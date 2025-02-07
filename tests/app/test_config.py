import os
from app.config import AppConfig
from unittest.mock import MagicMock, call, patch, PropertyMock, mock_open
import pytest


class TestAppConfig:

    def test_init_default(self):
        app_config = AppConfig()
        assert app_config.config_path is None
        assert app_config.config_file_path.endswith(AppConfig.DEFAULT_FILENAME)
        assert app_config.default_config["3cx"]["scheme"] == "https"
        assert app_config.default_config["app"]["logout_hotdesk_on_disable"] is True

    def test_init_with_config_path(self):
        config_path = "/custom/path"
        app_config = AppConfig(config_path=config_path)
        assert app_config.config_path == config_path
        assert app_config.config_file_path == os.path.join(config_path, AppConfig.DEFAULT_FILENAME)

    def test_server_url(self, app_config):
        app_config["3cx"] = {"scheme": "http", "domain": "example.com", "port": "8080"}
        expected_url = "http://example.com:8080"
        assert app_config.server_url == expected_url

    def test_is_dirty(self, app_config):
        app_config.set_original_config()
        assert app_config.is_dirty is False
        app_config.add_section("test")
        app_config.set("test", "test", "test")
        assert app_config.is_dirty is True

    def test_store_credential_security(self, app_config):
        app_config["3cx"] = {"store_credential_securely": True}
        assert app_config.store_credential_securely is True

    def test_logout_hotdesk_on_disable(self, app_config):
        app_config["app"] = {"logout_hotdesk_on_disable": True}
        assert app_config.logout_hotdesk_on_disable is True

    def test_load_defaults(self, app_config):
        app_config.read_dict = MagicMock()
        app_config.load_defaults()
        app_config.read_dict.assert_called_once_with(app_config.default_config)

    @patch("app.config.AppConfig.load_defaults")
    @patch("app.config.AppConfig.set_original_config")
    @patch("app.config.AppConfig.fetch_secure_credential")
    @patch("app.config.AppConfig.read")
    def test_load(
        self, mock_read, mock_fetch_secure_credential, mock_set_original_config, mock_load_defaults, app_config
    ):
        # config_file_path = "/test/path"
        # mock_config_file_path.return_value = config_file_path
        # mock_join.return_value = config_file_path
        app_config.config_file_path = "/test/path"
        app_config.load()
        mock_load_defaults.assert_called_once()
        mock_read.assert_called_once_with(app_config.config_file_path)
        mock_fetch_secure_credential.assert_called_once()
        mock_set_original_config.assert_called_once()

    @patch("app.config.AppConfig.set_original_config")
    @patch("app.config.AppConfig.store_secure_credential")
    @patch("app.config.AppConfig.write")
    @patch("builtins.open", new_callable=mock_open)
    def test_save(
        self,
        mock_open,
        mock_write,
        mock_store_secure_credential,
        mock_set_original_config,
        app_config,
    ):
        app_config.config_file_path = "/test/path"
        mock_file = MagicMock()
        mock_open.return_value = mock_file
        app_config.save()
        mock_store_secure_credential.assert_called_once()
        mock_open.assert_called_once_with(app_config.config_file_path, "w")
        mock_write.assert_called_once_with(mock_file.__enter__())
        mock_set_original_config.assert_called_once()

    @patch("app.config.AppConfig.set_original_config")
    @patch("app.config.AppConfig.write")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_to(self, mock_open, mock_write, mock_set_original_config, app_config):
        with patch("app.config.AppConfig.set_original_config") as mock_set_original_config:
            directory = "/test/path"

            mock_file = MagicMock()
            mock_open.return_value = mock_file
            app_config.save_to(directory)
            file_path = os.path.join(directory, app_config.DEFAULT_FILENAME)

            mock_open.assert_called_once_with(file_path, "w")
            mock_write.assert_called_once_with(mock_file.__enter__())
            mock_set_original_config.assert_not_called()

    @patch("app.config.deepcopy")
    def test_set_original_config(self, mock_deepcopy, app_config):
        app_config.load_defaults()
        mock_copy = MagicMock(spec=app_config)
        mock_deepcopy.return_value = mock_copy
        app_config.set_original_config()
        assert app_config.original_config == mock_copy

    def test_set_value_existing_section(self, app_config):
        app_config.add_section("test")
        app_config.set_value("test", "test", "test")
        assert app_config["test"]["test"] == "test"

    def test_set_value_new_section(self, app_config):
        app_config.set_value("test", "test", "test")
        assert app_config["test"]["test"] == "test"

    @patch("app.config.keyring")
    @patch.object(
        AppConfig,
        "store_credential_securely",
        new_callable=PropertyMock(return_value=True),
    )
    @patch.object(AppConfig, "get")
    @patch.object(AppConfig, "set")
    def test_fetch_secure_credential(
        self, mock_set, mock_get, mock_store_credential_securely_property, mock_keyring, app_config
    ):
        mock_get.return_value = "test_username"
        mock_keyring.get_password.return_value = "test_password"

        app_config.fetch_secure_credential()

        mock_get.assert_called_once_with("3cx", "username")
        mock_keyring.get_password.assert_called_once_with("3CX_Sync", "test_username")
        mock_set.assert_called_once_with("3cx", "password", "test_password")

    @patch("app.config.keyring")
    @patch.object(
        AppConfig,
        "store_credential_securely",
        new_callable=PropertyMock(return_value=False),
    )
    @patch.object(AppConfig, "set")
    def test_fetch_secure_credential_not_used(self, mock_set, mock_store_credential_securely, mock_keyring, app_config):
        app_config.fetch_secure_credential()
        mock_keyring.set_password.assert_not_called()
        mock_set.assert_not_called()

    @patch("app.config.keyring")
    @patch.object(
        AppConfig,
        "store_credential_securely",
        new_callable=PropertyMock(return_value=True),
    )
    @patch.object(AppConfig, "get")
    @patch.object(AppConfig, "set")
    def test_store_secure_credential_is_used(
        self,
        mock_set,
        mock_get,
        mock_store_credential_securely,
        mock_keyring,
        app_config,
    ):
        username = "test_username"
        password = "test_password"
        mock_get.side_effect = lambda section, key: {
            ("3cx", "username"): username,
            ("3cx", "password"): password,
        }.get((section, key), None)

        mock_keyring.get_password.return_value = password
        app_config.store_secure_credential()
        mock_keyring.set_password.assert_called_once_with("3CX_Sync", username, password)
        mock_set.assert_called_once_with("3cx", "password", None)

    @patch("app.config.keyring")
    @patch.object(
        AppConfig,
        "store_credential_securely",
        new_callable=PropertyMock(return_value=False),
    )
    @patch.object(AppConfig, "set")
    def test_store_secure_credential_not_used(self, mock_set, mock_store_credential_securely, mock_keyring, app_config):
        app_config.store_secure_credential()
        mock_keyring.set_password.assert_not_called()
        mock_set.assert_not_called()
