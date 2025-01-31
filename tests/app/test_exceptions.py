import pytest
from app.exceptions import ConfigSaveError


class TestConfigSaveError:

    def test_config_save_error(self):
        assert isinstance(ConfigSaveError(), Exception)

    def test_config_save_error_default_message(self):
        error = ConfigSaveError()
        with pytest.raises(ConfigSaveError):
            raise error
        assert error.message == "Failed to save the configuration file"

    def test_config_save_error_init(self):
        custom_message = "Error saving config"
        error = ConfigSaveError(custom_message)
        with pytest.raises(ConfigSaveError):
            raise error
        assert error.message == custom_message
