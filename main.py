import argparse
from app.app import App
from app.config import AppConfig
from sync.sync import run_sync
from sync.sync_strategy import SyncCSV
from sync.logging import LogLevel, SyncLogger


def get_app_args():
    parser = argparse.ArgumentParser(description="Process runtime arguments.")
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="Run without the GUI. Ensure mode is specified!",
    )
    parser.add_argument(
        "--mode",
        type=str,
        help='Sync mode to trigger on silent run. Options are: "CSV".',
    )
    return parser.parse_args()


def run_silent_mode(app_args: argparse.Namespace, logger: SyncLogger):
    """Runs the sync process in silent mode without GUI."""
    sync_source = SyncCSV if app_args.mode == "CSV" else None
    if sync_source:
        run_sync(sync_source=sync_source, logger=logger)
    else:
        logger.log(LogLevel.ERROR, "Invalid mode for silent sync")
        raise SystemExit("Invalid Arugments")


def run_gui_mode(logger: SyncLogger):
    """Runs the application in GUI mode"""
    app_config = AppConfig()
    app_config.load()
    app = App(logger=logger, app_config=app_config)
    app.mainloop()


def main():
    app_args = get_app_args()
    logger = SyncLogger()
    logger.add_file_handler()

    if app_args.silent:
        run_silent_mode(app_args, logger)
    else:
        run_gui_mode(logger)


if __name__ == "__main__":
    main()
