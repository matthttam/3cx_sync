from argparse import Namespace
import pytest
import sys
from unittest.mock import MagicMock, patch
from main import get_app_args, main, run_gui_mode, run_silent_mode
from sync.logging import SyncLogger


def test_get_app_args_no_args():
    test_args = ["main.py"]
    with patch.object(sys, "argv", test_args):
        args = get_app_args()
        assert not args.silent
        assert args.mode is None


def test_get_app_args_silent():
    test_args = ["main.py", "--silent"]
    with patch.object(sys, "argv", test_args):
        args = get_app_args()
        assert args.silent
        assert args.mode is None


def test_get_app_args_mode_csv():
    test_args = ["main.py", "--mode", "CSV"]
    with patch.object(sys, "argv", test_args):
        args = get_app_args()
        assert not args.silent
        assert args.mode == "CSV"


def test_get_app_args_silent_mode_csv():
    test_args = ["main.py", "--silent", "--mode", "CSV"]
    with patch.object(sys, "argv", test_args):
        args = get_app_args()
        assert args.silent
        assert args.mode == "CSV"


def test_get_app_args_invalid_mode():
    test_args = ["main.py", "--INVALID", "--MOREINVALID"]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            get_app_args()


def test_get_app_args_help():
    test_args = ["main.py", "--help"]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            get_app_args()


@patch("main.main")
def test_import_does_not_run_main(mock_main):
    import main

    mock_main.assert_not_called()


@patch("main.run_gui_mode")
@patch("main.run_silent_mode")
@patch("main.SyncLogger")
def test_main_silent_mode(mock_sync_logger_class, mock_run_silent_mode, mock_run_gui_mode):
    mock_sync_logger = MagicMock()
    test_args = ["main.py", "--silent", "--mode", "CSV"]
    mock_sync_logger_class.return_value = mock_sync_logger
    with patch.object(sys, "argv", test_args):
        main()

    mock_sync_logger.add_file_handler.assert_called_once()
    mock_run_silent_mode.assert_called_once_with(Namespace(silent=True, mode="CSV"), mock_sync_logger)
    mock_run_gui_mode.assert_not_called()


@patch("main.run_gui_mode")
@patch("main.run_silent_mode")
@patch("main.SyncLogger")
def test_main_gui_mode(mock_sync_logger_class, mock_run_silent_mode, mock_run_gui_mode):
    mock_sync_logger = MagicMock()
    test_args = ["main.py"]
    mock_sync_logger_class.return_value = mock_sync_logger
    with patch.object(sys, "argv", test_args):
        main()

    mock_sync_logger.add_file_handler.assert_called_once()
    mock_run_silent_mode.assert_not_called()
    mock_run_gui_mode.assert_called_once_with(mock_sync_logger)


def test_run_gui_mode():
    mock_logger = MagicMock(spec=SyncLogger)
    run_gui_mode
