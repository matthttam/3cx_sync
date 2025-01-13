import pytest
from app.mapping import CSVMapping
from collections import UserDict
from unittest.mock import patch, Mock, MagicMock, PropertyMock


class TestCSVMapping:

    @pytest.fixture
    def csv_mapping(self):
        yield CSVMapping()

    def test_mapping_subclass_userdict(self):
        assert issubclass(CSVMapping, UserDict)

    @patch("app.mapping.initialize_or_get_user_config_file")
    def test_config_file_path(self, mock_helper, csv_mapping):
        csv_mapping.mapping_file_path
        mock_helper.assert_called_once_with("3cx_sync", "3cx_sync", "conf", "csv_mapping.json")

    def test_is_dirty(self):
        ...

    @patch("app.mapping.os.getcwd")
    def test_mapping_file_path(self, mock_os_getcwd, csv_mapping):
        mock_os_getcwd.return_value = "/usr/var/test"
        mapping_file_path = csv_mapping.mapping_file_path
        assert mapping_file_path == "/usr/var/test/conf/csv_mapping.json"

    @patch("app.mapping.os.path.isfile", return_value=False)
    def test_validate_file_exists_if_file_missing_calls_initialize_mapping_file(
        self, mock_os_path_isfile, csv_mapping
    ):
        with patch.object(
            csv_mapping, "initialize_mapping_file", Mock()
        ) as mock_initialize_mapping_file:
            csv_mapping.validate_file_exists()
            mock_initialize_mapping_file.assert_called_once_with()

    @patch("app.mapping.os.path.isfile", return_value=True)
    def test_validate_file_exists_if_file_exists_does_not_call_initialize_mapping_file(
        self, mock_os_path_isfile, csv_mapping
    ):
        with patch.object(
            csv_mapping, "initialize_mapping_file", Mock()
        ) as mock_initialize_mapping_file:
            csv_mapping.validate_file_exists()
            mock_initialize_mapping_file.assert_not_called()

    @patch("app.mapping.os.path.isfile", return_value=True)
    @patch("app.mapping.os.stat", side_effect=lambda _: MagicMock(st_size=0))
    def test_validate_file_not_empty_if_file_empty_calls_initialize_mapping_file(
        self, mock_os_stat, mock_os_path_isfile, csv_mapping
    ):
        with patch.object(
            csv_mapping, "initialize_mapping_file", Mock()
        ) as mock_initialize_mapping_file:
            csv_mapping.validate_file_not_empty()
            mock_initialize_mapping_file.assert_called_once_with()

    @patch("app.mapping.os.path.isfile", return_value=True)
    @patch("app.mapping.os.stat", side_effect=lambda _: MagicMock(st_size=100))
    def test_validate_file_not_empty_if_file_not_empty_does_not_call_initialize_mapping_file(
        self, mock_os_stat, mock_os_path_isfile, csv_mapping
    ):
        with patch.object(
            csv_mapping, "initialize_mapping_file", Mock()
        ) as mock_initialize_mapping_file:
            csv_mapping.validate_file_not_empty()
            mock_initialize_mapping_file.assert_not_called()

    @patch.object(
        CSVMapping, "mapping_file_path", return_value="test", new_callable=PropertyMock
    )
    @patch.object(CSVMapping, "update")
    @patch("builtins.open", return_value=MagicMock())
    @patch("app.mapping.json.load", return_value={"A": "A", "B": "B"})
    def test_load_mapping_dict(
        self,
        mock_json_load,
        mock_open,
        mock_update,
        mock_mapping_file_path,
        csv_mapping,
    ):
        csv_mapping.load_mapping_dict()
        mock_file = mock_open.return_value.__enter__()
        mock_open.assert_called_once_with(mock_mapping_file_path.return_value, "r")
        mock_json_load.assert_called_once_with(mock_file)
        mock_file.close.assert_called_once_with()
        mock_update.assert_called_once_with(mock_json_load.return_value)

    @patch.object(
        CSVMapping, "mapping_file_path", return_value="test", new_callable=PropertyMock
    )
    @patch("builtins.open", return_value=MagicMock())
    def test_initialize_mapping_file(
        self, mock_open, mock_mapping_file_path, csv_mapping
    ):
        csv_mapping.initialize_mapping_file()
        mock_file = mock_open.return_value.__enter__()
        mock_open.assert_called_once_with(mock_mapping_file_path.return_value, "w")
        mock_file.write.assert_called_once_with("{}")
        mock_file.close.assert_called_once_with()

    @patch.object(
        CSVMapping, "mapping_file_path", return_value="test", new_callable=PropertyMock
    )
    @patch("builtins.open", return_value=MagicMock())
    @patch("app.mapping.json.dump")
    def test_save_mapping_config(
        self, mock_json_dump, mock_open, mock_mapping_file_path, csv_mapping
    ):
        mock_file = mock_open.return_value.__enter__()

        csv_mapping.save_mapping_config()
        with patch.dict(csv_mapping, {"A": "B", "C": "C"}) as data_dict:
            mock_open.assert_called_once_with(mock_mapping_file_path.return_value, "w")
            mock_json_dump.assert_called_once_with(data_dict, mock_file)
            mock_file.close.assert_called_once_with()

    def test_inverted_mapping(self, csv_mapping):
        items = {"A": "Apple", "B": "Banana", "C": "Cat"}
        inverted_items = {"Apple": "A", "Banana": "B", "Cat": "C"}
        assert csv_mapping.inverted_mapping(items) == inverted_items

    @patch.object(CSVMapping, "validate_file_exists")
    @patch.object(CSVMapping, "validate_file_not_empty")
    @patch.object(CSVMapping, "load_mapping_dict")
    def test_load_mapping_calls_validations_and_load_method(
        self,
        mock_load_mapping_dict,
        mock_validate_file_not_empty,
        mock_validate_file_exists,
        csv_mapping,
    ):
        csv_mapping.load_mapping_config()
        mock_validate_file_exists.assert_called_once_with()
        mock_validate_file_not_empty.assert_called_once_with()
        mock_load_mapping_dict.assert_called_once_with()
