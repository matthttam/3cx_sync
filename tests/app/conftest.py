import pytest
import tkinter as tk
from unittest.mock import MagicMock, patch
from app.windows import WindowAppConfig, WindowSync, Window, WindowCSVMapping
from app.config import AppConfig
from sync.logging import SyncLogger
from app.app import App


@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.quit()
    root.destroy()


@pytest.fixture
def mock_app_config(request):
    mock_app_config = MagicMock()
    if not hasattr(request, "param"):
        mock_app_config.get.return_value = ""
        mock_app_config.getboolean.return_value = False
    else:
        conf = request.param

        def get_side_effect(section, var):
            return conf.get(section, {}).get(var)

        mock_app_config.get.side_effect = get_side_effect
        mock_app_config.getboolean.side_effect = get_side_effect
    yield mock_app_config


@pytest.fixture
def window_app_config(root, mock_app_config):
    yield WindowAppConfig(master=root, app_config=mock_app_config)


@pytest.fixture
def window_csv_mapping(root):
    with patch("app.windows.CSVMapping", MagicMock()):
        yield WindowCSVMapping(master=root, csv_mapping=MagicMock())


@pytest.fixture
def window():
    yield Window()


@pytest.fixture
def app(mock_logger, mock_app_config):
    app = App(logger=mock_logger, app_config=mock_app_config)
    yield app
    app.quit()
    app.destroy()


@pytest.fixture
def window_sync(app):
    yield WindowSync(master=app)


@pytest.fixture()
def app_config():
    yield AppConfig()
