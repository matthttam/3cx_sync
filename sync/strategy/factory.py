from sync.logging import SyncLogger
from sync.strategy.strategy import SyncSourceStrategy


def create_sync_source(strategy_class: type[SyncSourceStrategy], logger: SyncLogger, **kwargs) -> SyncSourceStrategy:
    """Factory to create sync source instances with optional arguments."""
    return strategy_class(logger=logger, **kwargs)
