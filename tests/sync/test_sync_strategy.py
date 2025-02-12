from abc import ABC
from sync.strategy.factory import create_sync_source
from sync.strategy.csv.sync_csv import SyncCSV
from sync.strategy.strategy import SyncSourceStrategy
from sync.logging import SyncLogger, LogLevel
from unittest.mock import MagicMock, patch, mock_open, call
import pytest


class TestSyncSourceStrategy:

    def test_is_abc(self):
        assert issubclass(SyncSourceStrategy, ABC)


class TestSyncCSV:
    @pytest.fixture
    def mock_logger(self):
        return MagicMock(spec=SyncLogger)

    @pytest.fixture
    def sync_csv(self, mock_logger):
        return SyncCSV(logger=mock_logger)

    def test_initialize(self, sync_csv, mock_logger):
        with patch.object(sync_csv, "_load_csv_mapping") as mock_load_csv_mapping, patch.object(
            sync_csv, "_set_comparison_properties"
        ) as mock_set_comparison_properties:
            sync_csv.initialize()
            mock_load_csv_mapping.assert_called_once()
            mock_set_comparison_properties.assert_called_once()
            mock_logger.log.assert_any_call(LogLevel.INFO, "Initializing CSV Source")

    def test_load_csv_mapping(self, sync_csv):
        with patch("sync.sync_strategy.CSVMapping") as mock_csv_mapping:
            sync_csv._load_csv_mapping()
            mock_csv_mapping.assert_called_once()
            mock_csv_mapping.return_value.initialize.assert_called_once()
            sync_csv.logger.log.assert_has_calls(
                [
                    call(LogLevel.INFO, "Loading CSV Mapping"),
                    call(LogLevel.INFO, f"CSV Mapping Loaded from '{sync_csv.mapping.mapping_file_path}'"),
                ]
            )

    def test_set_comparison_properties(self, sync_csv, mock_logger):
        with patch("sync.sync_strategy.CSVUser.set_comparison_properties") as mock_set_comparison_properties:
            sync_csv.mapping = {"Extension": {"Update": ["field1", "field2"]}}
            sync_csv._set_comparison_properties()
            mock_set_comparison_properties.assert_called_once_with(["field1", "field2"])
            mock_logger.log.assert_any_call(LogLevel.INFO, "Comparison Properties Set")

    def test_get_source_users(self, sync_csv, mock_logger):
        with patch.object(
            sync_csv, "_get_csv_data_path", return_value="path/to/csv_file.csv"
        ) as mock_get_csv_data_path, patch.object(
            sync_csv,
            "_parse_csv_file",
            return_value=[{"field1": "value1", "field2": "value2"}],
        ) as mock_parse_csv_file, patch.object(
            sync_csv, "_validate_csv_users", return_value=["validated_user"]
        ) as mock_validate_csv_users:
            result = sync_csv.get_source_users()
            mock_get_csv_data_path.assert_called_once()
            mock_parse_csv_file.assert_called_once_with("path/to/csv_file.csv")
            mock_validate_csv_users.assert_called_once_with([{"field1": "value1", "field2": "value2"}])
            mock_logger.log.assert_any_call(LogLevel.INFO, "Loading CSV User Data")
            mock_logger.log.assert_any_call(LogLevel.INFO, "Loaded 1 Users from CSV File")
            assert result == ["validated_user"]

    def test_get_source_users_file_not_found(self, sync_csv, mock_logger):
        sync_csv.mapping = {"Extension": {"Path": "non_existent_file.csv"}}
        with pytest.raises(FileNotFoundError):
            sync_csv.get_source_users()
        mock_logger.log.assert_any_call(LogLevel.INFO, "Loading CSV User Data")
        mock_logger.log.assert_any_call(LogLevel.ERROR, "Unable to find file at: non_existent_file.csv")

    def test_get_csv_data_path(self, sync_csv):
        with patch("os.path.isfile", return_value=True):
            sync_csv.mapping = {"Extension": {"Path": "path/to/csv_file.csv"}}
            assert sync_csv._get_csv_data_path() == "path/to/csv_file.csv"

    def test_get_csv_data_path_file_not_found(self, sync_csv, mock_logger):
        with patch("os.path.isfile", return_value=False):
            sync_csv.mapping = {"Extension": {"Path": "non_existent_file.csv"}}
            with pytest.raises(FileNotFoundError):
                sync_csv._get_csv_data_path()
            mock_logger.log.assert_any_call(LogLevel.ERROR, "Unable to find file at: non_existent_file.csv")

    def test_parse_csv_file(self, sync_csv):
        csv_content = "header1,header2\nvalue1,value2\nvalue3,value4"
        with patch("builtins.open", new_callable=mock_open, read_data=csv_content):
            sync_csv.mapping = {"Extension": {"New": {"field1": "header1", "field2": "header2"}}}
            result = sync_csv._parse_csv_file("path/to/csv_file.csv")
            expected = [
                {"field1": "value1", "field2": "value2"},
                {"field1": "value3", "field2": "value4"},
            ]
            assert result == expected

    def test_parse_csv_file_with_disabled_user(self, sync_csv):
        csv_content = "header1,header2,Enabled\nvalue1,value2,0\nvalue3,value4,1"
        with patch("builtins.open", new_callable=mock_open, read_data=csv_content):
            sync_csv.mapping = {
                "Extension": {
                    "New": {
                        "field1": "header1",
                        "field2": "header2",
                        "Enabled": "Enabled",
                    }
                }
            }
            result = sync_csv._parse_csv_file("path/to/csv_file.csv")
            expected = [
                {
                    "field1": "value1",
                    "field2": "value2",
                    "Enabled": "0",
                    "HotdeskingAssignment": "",
                },
                {"field1": "value3", "field2": "value4", "Enabled": "1"},
            ]
            assert result == expected

    def test_validate_csv_users(self, sync_csv):
        user_data = [{"field1": "value1", "field2": "value2"}]
        with patch(
            "sync.sync_strategy.TypeAdapter.validate_python",
            return_value=["validated_user"],
        ) as mock_validate:
            result = sync_csv._validate_csv_users(user_data)
            mock_validate.assert_called_once_with(user_data)
            assert result == ["validated_user"]

    def test_get_user_update_fields(self, sync_csv):
        sync_csv.mapping = {"Extension": {"Update": ["field1", "field2"]}}
        assert sync_csv.get_user_update_fields() == ["field1", "field2"]

    def test_get_source_groups(self, sync_csv):
        assert sync_csv.get_source_groups() is None


@patch("sync.sync_strategy.SyncCSV", spec=SyncCSV)
def test_create_sync_source_sync_csv(mock_sync_cvs_class, mock_logger):
    mock_sync_csv = MagicMock()
    mock_sync_cvs_class.return_value = mock_sync_csv
    response = create_sync_source(strategy_class=mock_sync_cvs_class, logger=mock_logger)
    assert response == mock_sync_csv
    mock_sync_cvs_class.assert_called_once_with(config_path=None, logger=mock_logger)


@patch("sync.sync_strategy.SyncCSV", spec=SyncCSV)
def test_create_sync_source_sync_csv_with_config_path(mock_sync_cvs_class, mock_logger):
    mock_sync_csv = MagicMock()
    mock_sync_cvs_class.return_value = mock_sync_csv
    response = create_sync_source(strategy_class=mock_sync_cvs_class, logger=mock_logger, config_path="/test/path")
    assert response == mock_sync_csv
    mock_sync_cvs_class.assert_called_once_with(config_path="/test/path", logger=mock_logger)


def test_create_sync_source_other(mock_logger):
    response = create_sync_source(strategy_class=MagicMock, logger=mock_logger)
