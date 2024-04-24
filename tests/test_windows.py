import pytest
import tkinter as tk
from unittest.mock import patch, MagicMock
from app.windows import Window3cxConfig
# from tcx_api.tcx_api_connection import TCX_API_Connection
from app.config import TCXConfig
from tests.test_config import tcx_config


class TestWindow3cxConfig:
    @pytest.fixture
    def root(self):
        root = tk.Tk()
        yield root

    @pytest.fixture
    def mock_tcx_config(self):
        yield MagicMock(spec=TCXConfig)

    @pytest.fixture
    def window(self, root, mock_tcx_config):
        yield Window3cxConfig(master=root, tcx_config=mock_tcx_config)

    @patch.object(Window3cxConfig, 'build_gui')
    @patch.object(Window3cxConfig, 'initialize_variables')
    def test_init(self, mock_initialize_variables, mock_build_gui, root):
        window = Window3cxConfig(
            master=root, tcx_config=MagicMock(spec=TCXConfig))
        assert isinstance(window, Window3cxConfig)
        # assert window.tcx_config == 1
        window.tcx_config.load.assert_called_once_with()
        mock_initialize_variables.assert_called_once_with()
        mock_build_gui.assert_called_once_with()

    @patch('app.config.TCXConfig')
    def test_initialize_variables_blank(self, mock_tcx_config, root):
        conf = {"3cx": {
            "scheme": None,
            "domain": None,
            "port": None,
            "username": None,
            "password": None
        }}
        mock_tcx_config.__getitem__.side_effect = conf.__getitem__
        window = Window3cxConfig(master=root, tcx_config=mock_tcx_config)
        assert isinstance(window.vars, dict)

        for k in conf["3cx"].keys():
            assert isinstance(window.vars[k], tk.StringVar)
            assert window.vars[k].get() == ""

    @patch('app.config.TCXConfig')
    def test_initialize_variables_with_values(self, mock_tcx_config, root):
        # with patch.object(window, 'tcx_config', {"3cx": {"scheme": "test_scheme", "domain": "test_domain", "port": "", "username": "", "password": ""}}) as tcx_config:
        # tcx_config = TCXConfig()
        conf = {"3cx": {
            "scheme": "test_scheme",
            "domain": "test_domain",
            "port": "test_port",
            "username": "username",
            "password": "password"
        }}
        mock_tcx_config.__getitem__.side_effect = conf.__getitem__
        window = Window3cxConfig(master=root, tcx_config=mock_tcx_config)
        assert isinstance(window.vars, dict)

        for k in conf["3cx"].keys():
            assert isinstance(window.vars[k], tk.StringVar)
            assert window.vars[k].get() == conf["3cx"][k]

    @patch('tcx_api.tcx_api_connection.TCX_API_Connection')
    def test_test_connection_success(self, mock_api):
        mock_api_instance = mock_api.return_value
        self.window.var_3cx_scheme.set('https')
        self.window.var_3cx_domain.set('example.com')
        self.window.var_3cx_port.set('8080')
        self.window.var_3cx_username.set('user')
        self.window.var_3cx_password.set('password')

        # Configure the mock to succeed
        mock_api_instance.authenticate.return_value = True

        # Call the method to test
        self.window.test_connection()

        # Assert that the success message is shown
        self.assertTrue(self.window.messagebox.showinfo.called)

    @patch('tcx_api.tcx_api_connection.TCX_API_Connection')
    def test_test_connection_failure(self, mock_api):
        mock_api_instance = mock_api.return_value
        self.window.var_3cx_scheme.set('https')
        self.window.var_3cx_domain.set('example.com')
        self.window.var_3cx_port.set('8080')
        self.window.var_3cx_username.set('user')
        self.window.var_3cx_password.set('password')

        # Configure the mock to raise an exception
        mock_api_instance.authenticate.side_effect = Exception(
            'Authentication failed')

        # Call the method to test
        self.window.test_connection()

        # Assert that the failure message is shown
        self.assertTrue(self.window.messagebox.showinfo.called)

    @patch('your_module.TCXConfig')
    def test_write_config_file(self, mock_tcx_config):
        mock_config_instance = mock_tcx_config.return_value
        self.window.var_3cx_scheme.set('https')
        self.window.var_3cx_domain.set('example.com')
        self.window.var_3cx_port.set('8080')
        self.window.var_3cx_username.set('user')
        self.window.var_3cx_password.set('password')

        # Call the method to test
        self.window.write_config_file()

        # Assert that the TCXConfig instance is updated
        self.assertEqual(mock_config_instance['3cx']['scheme'], 'https')
        self.assertEqual(mock_config_instance['3cx']['domain'], 'example.com')
        self.assertEqual(mock_config_instance['3cx']['port'], '8080')
        self.assertEqual(mock_config_instance['3cx']['username'], 'user')
        self.assertEqual(mock_config_instance['3cx']['password'], 'password')
