from app.app import App
import argparse
from sync.logging import SyncLogger
from app.config import AppConfig
from sync.sync import run_sync
from sync.sync_strategy import SyncCSV


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


if __name__ == "__main__":
    app_args = get_app_args()
    logger = SyncLogger()
    logger.add_file_handler()

    if app_args.silent:
        if app_args.mode == "CSV":
            sync_source = SyncCSV
        run_sync(sync_source=sync_source, logger=logger)

    else:
        app_config = AppConfig()
        app_config.load()
        app = App(logger=logger, app_config=app_config)
        app.mainloop()
