import sys
from argparse import Namespace
import pytest
from argparse import ArgumentParser, Namespace
from unittest.mock import MagicMock, patch
from app.config import AppConfig
from main import dir_path, get_app_args, main, run_gui_mode, run_silent_mode, App
from sync.logging import SyncLogger


@pytest.mark.parametrize(
    "silent_mode, expected_called_func",
    [
        (None, "run_gui_mode"),  # GUI mode → Calls run_gui_mode(logger)
        (False, "run_gui_mode"),  # GUI mode → Calls run_gui_mode(logger)
        (True, "run_silent_mode"),  # Silent mode → Calls run_silent_mode(app_args, logger)
    ],
)
@patch("main.run_gui_mode")
@patch("main.run_silent_mode")
@patch("main.SyncLogger")
@patch("main.get_app_args")
def test_main(
    mock_get_app_args,
    mock_sync_logger_class,
    mock_run_silent_mode,
    mock_run_gui_mode,
    silent_mode,
    expected_called_func,
):
    mock_sync_logger = MagicMock(spec=SyncLogger)
    mock_sync_logger_class.return_value = mock_sync_logger
    mock_app_args = MagicMock(spec=Namespace)
    mock_app_args.silent = silent_mode
    mock_app_args.config_path = "/test/path"
    mock_get_app_args.return_value = mock_app_args

    from main import main

    main()

    mock_get_app_args.assert_called_once()
    mock_sync_logger.add_file_handler.assert_called_once()

    if expected_called_func == "run_gui_mode":
        mock_run_silent_mode.assert_not_called()
        mock_run_gui_mode.assert_called_once_with(logger=mock_sync_logger, config_path=mock_app_args.config_path)
    else:
        mock_run_silent_mode.assert_called_once_with(mock_app_args, mock_sync_logger)
        mock_run_gui_mode.assert_not_called()


@patch("main.main")
def test_import_does_not_run_main(mock_main):
    import main

    mock_main.assert_not_called()


@patch.object(sys, "argv", ["main.py", "--silent", "--mode", "CSV"])
def test_get_app_args():
    args = get_app_args()
    assert args == Namespace(silent=True, mode="CSV", config_path=None)


@patch.object(sys, "argv", ["main.py", "--silent"])
def test_get_app_args_invalid_combination():
    with pytest.raises(SystemExit):
        get_app_args()


@pytest.mark.parametrize(
    "mode, config_path",
    [
        ("CSV", "/test/path/"),  # CSV mode should run_sync with SyncCSV
        ("INVALID", None),  # INVALID mode shoudl log and error
    ],
)
@patch("main.SyncCSV")
@patch("main.run_sync")
def test_run_silent_mode(mock_run_sync, mock_sync_csv_class, mode, config_path):
    mock_logger = MagicMock(spec=SyncLogger)
    args = Namespace(mode=mode, config_path=config_path)

    if mode == "INVALID":
        with pytest.raises(SystemExit):
            run_silent_mode(args, mock_logger)
        mock_run_sync.assert_not_called()
        return

    if mode == "CSV":
        run_silent_mode(args, mock_logger)
        mock_run_sync.assert_called_once_with(
            sync_source_class=mock_sync_csv_class, logger=mock_logger, config_path=config_path
        )


@patch("main.App")
@patch("main.AppConfig")
def test_run_gui_mode(mock_app_config_class, mock_app_class):
    mock_logger = MagicMock(spec=SyncLogger)
    mock_app_config = MagicMock(spec=AppConfig)
    mock_app_config_class.return_value = mock_app_config
    mock_app = MagicMock(spec=App)
    mock_app_class.return_value = mock_app

    run_gui_mode(mock_logger)

    mock_app_config.load.assert_called_once()
    mock_app_class.assert_called_once_with(logger=mock_logger, app_config=mock_app_config)
    mock_app.mainloop.assert_called_once()


@patch("main.os.path.isdir")
def test_dir_path(mock_isdir):
    mock_isdir.return_value = True
    result = dir_path("/test/path/")
    assert result == "/test/path/"


@patch("main.os.path.isdir")
def test_dir_path_invalid_path(mock_isdir):
    mock_isdir.return_value = False
    with pytest.raises(NotADirectoryError):
        result = dir_path("/test/path/")
        assert result is None
