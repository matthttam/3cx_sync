import json
import pytest
from pathlib import Path
from sync.strategy.csv.mapping import CSVMapping
from collections import UserDict
from unittest.mock import patch, MagicMock, mock_open


class TestCSVMapping:

    # test_path = Path("/test/path")

    @pytest.fixture
    def mock_path(self):
        path = MagicMock(spec=Path)
        yield path

    @pytest.fixture
    def csv_mapping(self, mock_path):
        yield CSVMapping(config_path=mock_path)

    def test_init(self):
        test_path = Path("/test/path")
        csv_mapping = CSVMapping(config_path=test_path)
        assert issubclass(CSVMapping, UserDict)
        assert csv_mapping.mapping_file_path == test_path / CSVMapping.DEFAULT_FILENAME
        assert csv_mapping.default_config is not None
        assert csv_mapping.original_config == {}

    @patch.object(CSVMapping, "load_defaults")
    @patch.object(CSVMapping, "load")
    def test_initialize(self, mock_load, mock_load_defaults, csv_mapping):
        csv_mapping.initialize()
        mock_load_defaults.assert_called_once()
        mock_load.assert_called_once()

    @patch.object(CSVMapping, "load_defaults")
    @patch.object(CSVMapping, "load")
    def test_initialize_no_file_does_not_loa(self, mock_load, mock_load_defaults, csv_mapping):
        csv_mapping.mapping_file_path.exists.return_value = False
        csv_mapping.initialize()
        mock_load_defaults.assert_called_once()
        mock_load.assert_not_called()

        csv_mapping.load()

    def test_is_dirty(self, csv_mapping):
        csv_mapping.load_defaults()
        csv_mapping.set_original_config()
        assert csv_mapping.is_dirty is False
        csv_mapping.data["Key"] = "New_KEY"
        assert csv_mapping.is_dirty is True

    def test_load_defaults(self, csv_mapping):
        assert csv_mapping.data == {}
        csv_mapping.load_defaults()
        assert csv_mapping.data == csv_mapping.default_config

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_successful(self, mock_open, csv_mapping):
        csv_mapping.update = MagicMock()
        csv_mapping.mapping_file_path.stat = MagicMock(return_value=MagicMock(st_size=10))

        csv_mapping.set_original_config = MagicMock()
        csv_mapping.load()
        csv_mapping.update.assert_called_once_with({"key": "value"})
        csv_mapping.set_original_config.assert_called_once()
        mock_open.assert_called_once_with(csv_mapping.mapping_file_path, "r")

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_load_invalid_json(self, mock_open, csv_mapping):
        csv_mapping.mapping_file_path.stat = MagicMock(return_value=MagicMock(st_size=10))
        with pytest.raises(json.JSONDecodeError):
            csv_mapping.load()
        mock_open.assert_called_once_with(csv_mapping.mapping_file_path, "r")

    @patch("builtins.open", new_callable=mock_open)
    def test_load_file_not_found(self, mock_open, csv_mapping):
        csv_mapping.set_original_config = MagicMock()
        csv_mapping.mapping_file_path.exists = MagicMock(return_value=False)
        
        csv_mapping.load()

        assert csv_mapping.data == {}
        csv_mapping.set_original_config.assert_not_called()
        mock_open.assert_not_called()

    #@patch("app.mapping.json")
    @patch("sync.strategy.csv.mapping.json")
    @patch("builtins.open", new_callable=mock_open)
    def test_save(self, mock_open, mock_json, csv_mapping):
        fake_data = {"key": "value"}
        csv_mapping.data = fake_data
        mock_json.dump.return_value = json.dumps(fake_data)
        csv_mapping.set_original_config = MagicMock()
        csv_mapping.save()
        mock_open.assert_called_once_with(csv_mapping.mapping_file_path, "w")
        mock_json.dump.assert_called_once_with(fake_data, mock_open())
        csv_mapping.set_original_config.assert_called_once()

    @patch("sync.strategy.csv.mapping.json")
    @patch("sync.strategy.csv.mapping.Path.open")
    def test_save_to(self, mock_path_open, mock_json, csv_mapping):
        path = "/another/test/path"

        fake_data = {"key": "value"}
        csv_mapping.data = fake_data
        mock_json.dump.return_value = json.dumps(fake_data)
        csv_mapping.set_original_config = MagicMock()

        csv_mapping.save_to(path)

        mock_path_open.assert_called_once_with("w")
        mock_json.dump.assert_called_once_with(fake_data, mock_path_open().__enter__())

    def test_set_original_config(self, csv_mapping):
        csv_mapping.data = {"key": "value"}
        csv_mapping.original_config = {"blah": "blah"}
        csv_mapping.set_original_config()
        assert csv_mapping.original_config == {"key": "value"}

    def test_get_parsed_config(self, csv_mapping):
        csv_mapping.update(
            {
                "Extension": {
                    "Path": "/Fake/Path",
                    "Key": "Number",
                    "New": {
                        "Number": "Number",
                        "FirstName": "FirstName",
                        "LastName": "LastName",
                        "EmailAddress": "Email",
                        "VMPIN": "VMPIN",
                        "VMEmailOptions": "VMEmailOptions",
                        "OutboundCallerID": "OutboundCallerID",
                        "SendEmailMissedCalls": "SendEmailMissedCalls",
                        "Enabled": "Enabled",
                        "EnableHotdesking": "AllowToUseHotdesking",
                        "RecordCalls": "RecordCalls",
                        "RecordExternalCallsOnly": "RecordExternalCallsOnly",
                        "VMEnabled": "VMEnabled",
                        "WebMeetingFriendlyName": "WebMeetingFriendlyName",
                    },
                    "Update": ["FirstName", "LastName", "EmailAddress", "Enabled"],
                }
            }
        )

        expected_value = [
            {"header": "Number", "field": "Number", "static": False, "key": True, "update": False},
            {"header": "FirstName", "field": "FirstName", "static": False, "key": False, "update": True},
            {"header": "LastName", "field": "LastName", "static": False, "key": False, "update": True},
            {"header": "Email", "field": "EmailAddress", "static": False, "key": False, "update": True},
            {"header": "VMPIN", "field": "VMPIN", "static": False, "key": False, "update": False},
            {"header": "VMEmailOptions", "field": "VMEmailOptions", "static": False, "key": False, "update": False},
            {"header": "OutboundCallerID", "field": "OutboundCallerID", "static": False, "key": False, "update": False},
            {
                "header": "SendEmailMissedCalls",
                "field": "SendEmailMissedCalls",
                "static": False,
                "key": False,
                "update": False,
            },
            {"header": "Enabled", "field": "Enabled", "static": False, "key": False, "update": True},
            {
                "header": "AllowToUseHotdesking",
                "field": "EnableHotdesking",
                "static": False,
                "key": False,
                "update": False,
            },
            {"header": "RecordCalls", "field": "RecordCalls", "static": False, "key": False, "update": False},
            {
                "header": "RecordExternalCallsOnly",
                "field": "RecordExternalCallsOnly",
                "static": False,
                "key": False,
                "update": False,
            },
            {"header": "VMEnabled", "field": "VMEnabled", "static": False, "key": False, "update": False},
            {
                "header": "WebMeetingFriendlyName",
                "field": "WebMeetingFriendlyName",
                "static": False,
                "key": False,
                "update": False,
            },
        ]
        assert csv_mapping.get_parsed_config() == expected_value

    def test_restore_original_config(self, csv_mapping):
        csv_mapping.data = {"key": "value"}
        csv_mapping.original_config = {"original_key": "original_value"}
        csv_mapping.restore_original_config()
        assert csv_mapping.data == {"original_key": "original_value"}
        assert csv_mapping.original_config == {"original_key": "original_value"}