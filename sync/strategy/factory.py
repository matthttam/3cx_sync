from sync.logging import SyncLogger
from sync.strategy.csv.sync_csv import SyncCSV
from sync.strategy.strategy import SyncSourceStrategy


def create_sync_source(strategy_class: type[SyncSourceStrategy], logger: SyncLogger, **kwargs) -> SyncSourceStrategy:
    """Factory to create sync source instances with optional arguments."""
    if strategy_class is SyncCSV:
        return SyncCSV(config_path=kwargs.get("config_path"), logger=logger)
    return strategy_class(logger=logger)  # Default case for other strategies
