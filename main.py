from app.app import App
import argparse
from sync.logging import SyncLogger
from app.config import AppConfig


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
    sync_logger = SyncLogger()
    sync_logger.addFileHandler()
    if not app_args.silent:
        app = App(sync_logger=sync_logger, app_config=AppConfig())
        app.mainloop()
    else:
        pass
