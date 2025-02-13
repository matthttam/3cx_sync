import os
import traceback
from argparse import ArgumentParser, Namespace
from app.app import App
from app.config import AppConfig
from sync.sync import run_sync
from sync.strategy.csv.sync_csv import SyncCSV
from sync.logging import LogLevel, SyncLogger

import sv_ttk


def dir_path(path: str):
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)


def get_app_args():
    parser = ArgumentParser(description="Process runtime arguments.")
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="Run without the GUI. Requires --mode.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        help='Sync mode to trigger on silent run. Options are: "CSV".',
    )
    parser.add_argument(
        "-c", "--config_path", type=dir_path, help="Path to config folder containing app config and mapping files."
    )
    args = parser.parse_args()
    if args.silent and args.mode is None:
        raise parser.error("--silent requires --mode")
    return args


def run_silent_mode(app_args: Namespace, logger: SyncLogger):
    """Runs the sync process in silent mode without GUI."""
    sync_source_class = None

    if app_args.mode == "CSV":
        sync_source_class = SyncCSV
    if sync_source_class:
        run_sync(sync_source_class=sync_source_class, logger=logger, config_path=app_args.config_path)
    else:
        logger.log(LogLevel.ERROR, "Invalid mode for silent sync")
        raise SystemExit("Invalid Arugments")


def run_gui_mode(logger: SyncLogger, config_path: str = None):
    """Runs the application in GUI mode"""
    app_config = AppConfig(config_path=config_path)
    app_config.load()
    app = App(logger=logger, app_config=app_config)
    # sv_ttk.set_theme("dark")
    app.mainloop()


def main():
    logger = SyncLogger()
    logger.add_file_handler()

    try:
        app_args = get_app_args()
        if app_args.silent:
            run_silent_mode(app_args, logger)
        else:

            run_gui_mode(logger=logger, config_path=app_args.config_path)
    except Exception as e:
        logger.log(LogLevel.CRITICAL, f"A critical error has occured and the application must exit. {e}")
        logger.log(LogLevel.CRITICAL, f"Traceback: {traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main()
