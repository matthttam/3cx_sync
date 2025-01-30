import os
import json
import pytest
from app.mapping import CSVMapping
from collections import UserDict
from unittest.mock import patch, MagicMock, mock_open


class TestCSVMapping:

    test_path = "/test/path"

    @pytest.fixture
    def csv_mapping(self):
        yield CSVMapping(mapping_file_path=self.test_path)

    def test_init(self):
        csv_mapping = CSVMapping(mapping_file_path=self.test_path)
        assert issubclass(CSVMapping, UserDict)
        assert csv_mapping.mapping_file_path == self.test_path
        assert csv_mapping.default_config is not None
        assert csv_mapping.original_config == {}

    @patch.object(CSVMapping, "load_defaults")
    @patch.object(CSVMapping, "load")
    def test_initialize(self, mock_load, mock_load_defaults, csv_mapping):
        csv_mapping.initialize()
        mock_load_defaults.assert_called_once_with()
        mock_load.assert_called_once_with()

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
    @patch("os.path.getsize", return_value=10)
    def test_load_successful(self, mock_getsize, mock_open, csv_mapping):
        csv_mapping.update = MagicMock()
        csv_mapping.set_original_config = MagicMock()
        csv_mapping.load()
        csv_mapping.update.assert_called_once_with({"key": "value"})
        csv_mapping.set_original_config.assert_called_once()

    @patch("os.path.getsize", side_effect=FileNotFoundError)
    def test_load_file_not_found(self, mock_getsize, csv_mapping):
        with pytest.raises(FileNotFoundError):
            csv_mapping.load()

    @patch("builtins.open", new_callable=mock_open, read_data="")
    @patch("os.path.getsize", return_value=0)
    def test_load_empty_file(self, mock_getsize, mock_open, csv_mapping):
        with patch("builtins.print") as mocked_print:
            csv_mapping.load()
            mocked_print.assert_called_once_with(f"Warning: {self.test_path} is empty.")

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    @patch("os.path.getsize", return_value=10)
    def test_load_invalid_json(self, mock_getsize, mock_open, csv_mapping):
        with pytest.raises(json.JSONDecodeError):
            csv_mapping.load()

    @patch("app.mapping.json")
    @patch("builtins.open", new_callable=mock_open)
    def test_save(self, mock_open, mock_json, csv_mapping):
        fake_data = {"key": "value"}
        csv_mapping.data = fake_data
        mock_json.dump.return_value = json.dumps(fake_data)
        csv_mapping.set_original_config = MagicMock()
        csv_mapping.save()
        mock_open.assert_called_once_with(self.test_path, "w")
        mock_json.dump.assert_called_once_with(fake_data, mock_open())
        csv_mapping.set_original_config.assert_called_once()

    @patch("app.mapping.json")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_to(self, mock_open, mock_json, csv_mapping):
        path = "/another/test/path"

        fake_data = {"key": "value"}
        csv_mapping.data = fake_data
        mock_json.dump.return_value = json.dumps(fake_data)
        csv_mapping.set_original_config = MagicMock()

        csv_mapping.save_to(path)

        mock_open.assert_called_once_with(os.path.join(path, CSVMapping.DEFAULT_FILENAME), "w")
        mock_json.dump.assert_called_once_with(fake_data, mock_open())

    def test_set_original_config(self, csv_mapping):
        csv_mapping.data = {"key": "value"}
        csv_mapping.original_config = {"blah": "blah"}
        csv_mapping.set_original_config()
        assert csv_mapping.original_config == {"key": "value"}
