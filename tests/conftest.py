from unittest.mock import MagicMock
import pytest

from sync.logging import SyncLogger


@pytest.fixture
def mock_logger():
    yield MagicMock(spec=SyncLogger)
