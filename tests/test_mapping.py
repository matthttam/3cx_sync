from app.mapping import CSVMapping
from collections import UserDict
import csv
from unittest.mock import patch, Mock, MagicMock, PropertyMock, DEFAULT
import pytest


class TestCSVMapping:

    @pytest.fixture
    def csv_mapping(self):
        yield CSVMapping()

    def test_mapping_subclass_userdict(self):
        assert issubclass(CSVMapping, UserDict)

    @patch('app.mapping.os.getcwd')
    def test_mapping_file_path(self, mock_os_getcwd, csv_mapping):
        mock_os_getcwd.return_value = '/usr/var/test'
        mapping_file_path = csv_mapping.mapping_file_path
        assert mapping_file_path == '/usr/var/test/conf/csv_mapping.json'

    @patch('app.mapping.os.path.isfile', return_value=False)
    def test_validate_file_exists_if_file_missing_calls_initialize_mapping_file(self, mock_os_path_isfile, csv_mapping):
        with patch.object(csv_mapping, "initialize_mapping_file", Mock()) as mock_initialize_mapping_file:
            csv_mapping.validate_file_exists()
            mock_initialize_mapping_file.assert_called_once_with()

    @patch('app.mapping.os.path.isfile', return_value=True)
    def test_validate_file_exists_if_file_exists_does_not_call_initialize_mapping_file(self, mock_os_path_isfile, csv_mapping):
        with patch.object(csv_mapping, "initialize_mapping_file", Mock()) as mock_initialize_mapping_file:
            csv_mapping.validate_file_exists()
            mock_initialize_mapping_file.assert_not_called()

    @patch('app.mapping.os.path.isfile', return_value=True)
    @patch('app.mapping.os.stat', side_effect=lambda _: MagicMock(st_size=0))
    def test_validate_file_not_empty_if_file_empty_calls_initialize_mapping_file(self, mock_os_stat, mock_os_path_isfile, csv_mapping):
        with patch.object(csv_mapping, "initialize_mapping_file", Mock()) as mock_initialize_mapping_file:
            csv_mapping.validate_file_not_empty()
            mock_initialize_mapping_file.assert_called_once_with()

    @patch('app.mapping.os.path.isfile', return_value=True)
    @patch('app.mapping.os.stat', side_effect=lambda _: MagicMock(st_size=100))
    def test_validate_file_not_empty_if_file_not_empty_does_not_call_initialize_mapping_file(self, mock_os_stat, mock_os_path_isfile, csv_mapping):
        with patch.object(csv_mapping, "initialize_mapping_file", Mock()) as mock_initialize_mapping_file:
            csv_mapping.validate_file_not_empty()
            mock_initialize_mapping_file.assert_not_called()

    @patch.object(CSVMapping, 'mapping_file_path', return_value='test', new_callable=PropertyMock)
    @patch.object(CSVMapping, 'update')
    @patch('builtins.open', return_value=MagicMock())
    @patch('app.mapping.json.load', return_value={"A": "A", "B": "B"})
    def test_load_mapping_dict(self, mock_json_load, mock_open, mock_update, mock_mapping_file_path, csv_mapping):
        csv_mapping.load_mapping_dict()
        mock_file = mock_open.return_value.__enter__()
        mock_open.assert_called_once_with(
            mock_mapping_file_path.return_value, 'r')
        mock_json_load.assert_called_once_with(mock_file)
        mock_file.close.assert_called_once_with()
        mock_update.assert_called_once_with(mock_json_load.return_value)

    @patch.object(CSVMapping, 'mapping_file_path', return_value='test', new_callable=PropertyMock)
    @patch('builtins.open', return_value=MagicMock())
    def test_initialize_mapping_file(self, mock_open, mock_mapping_file_path, csv_mapping):
        csv_mapping.initialize_mapping_file()
        mock_file = mock_open.return_value.__enter__()
        mock_open.assert_called_once_with(
            mock_mapping_file_path.return_value, 'w')
        mock_file.write.assert_called_once_with("{}")
        mock_file.close.assert_called_once_with()

    # @patch.object(CSVMapping, 'data', return_value={"A": "B", "C": "C"})
    @patch.object(CSVMapping, 'mapping_file_path', return_value='test', new_callable=PropertyMock)
    @patch('builtins.open', return_value=MagicMock())
    @patch('app.mapping.json.dump')
    def test_save_mapping_config(self, mock_json_dump, mock_open, mock_mapping_file_path, csv_mapping):
        mock_file = mock_open.return_value.__enter__()

        csv_mapping.save_mapping_config()
        # with patch.object(csv_mapping, 'data', MagicMock(spec=UserDict, return_value={"A": "B", "C": "C"})) as data_dict:
        with patch.dict(csv_mapping, {"A": "B", "C": "C"}) as data_dict:
            mock_open.assert_called_once_with(
                mock_mapping_file_path.return_value, 'w')
            # mock_json_dumps.called_once_with(            csv_mapping.__dict__["data"], mock_file)
            mock_json_dump.assert_called_once_with(
                data_dict, mock_file)
            mock_file.close.assert_called_once_with()

    def test_inverted_mapping(self, csv_mapping):
        items = {"A": "Apple", "B": "Banana", "C": "Cat"}
        inverted_items = {"Apple": "A", "Banana": "B", "Cat": "C"}
        assert csv_mapping.inverted_mapping(items) == inverted_items
        # mock_update.assert_called_once()
        # mock_mapping_file_path.assert_called_once_with()

        # mock_mapping_file_path.assert_

        # with patch("app.mapping.CSVMapping.initialize_mapping_file", MagicMock()) as mock_initialize_mapping_file:
        #    with patch("app.mapping.CSVMapping.mapping_file_path", new_callable=PropertyMock) as mock_mapping_file_path:
        #        mock_mapping_file_path.return_value = "TEST_PATH"
        # with patch.multiple('app.mapping.csv_mapping', initialize_mapping_file=MagicMock(), mapping_file_path="TEST_PATH") as mocks:
        #        csv_mapping.load_mapping()
        #        mock_os_path_isfile.assert_called_once()
        #        mock_os_stat.assert_called_once()
        #        mock_initialize_mapping_file.assert_called_once_with()

    @ patch.object(CSVMapping, 'validate_file_exists')
    @ patch.object(CSVMapping, 'validate_file_not_empty')
    @ patch.object(CSVMapping, 'load_mapping_dict')
    def test_load_mapping_calls_validations_and_load_method(self, mock_load_mapping_dict, mock_validate_file_not_empty, mock_validate_file_exists, csv_mapping):
        csv_mapping.load_mapping_config()
        mock_validate_file_exists.assert_called_once_with()
        mock_validate_file_not_empty.assert_called_once_with()
        mock_load_mapping_dict.assert_called_once_with()
