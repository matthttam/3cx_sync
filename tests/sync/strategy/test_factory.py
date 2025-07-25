from unittest.mock import MagicMock
from sync.strategy.factory import create_sync_source

def test_create_sync_source_instantiates_with_logger_and_kwargs(mock_logger):
    mock_instance = MagicMock()
    mock_strategy_class = MagicMock(return_value=mock_instance)

    result = create_sync_source(
        strategy_class=mock_strategy_class,
        logger=mock_logger,
        foo="bar",
        another=123
    )

    mock_strategy_class.assert_called_once_with(logger=mock_logger, foo="bar", another=123)
    assert result is mock_instance
