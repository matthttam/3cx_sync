import pytest
import tkinter as tk
from unittest.mock import patch, MagicMock, call, DEFAULT
from app.windows import Window3cxConfig
# from tcx_api.tcx_api_connection import TCX_API_Connection
from app.config import TCXConfig
from tests.test_config import tcx_config
from app.exceptions import ConfigSaveError


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

    @patch('app.windows.tk.Button')
    def test_button_function_mapping(self, mock_button, mock_tcx_config, root):
        window = Window3cxConfig(master=root, tcx_config=mock_tcx_config)
        calls = [call(master=window.widgets["frm_navigation"], name="btn_test", text="Test",
                      command=window.handle_test_connection),
                 call(master=window.widgets["frm_navigation"], name="btn_save", text="Save",
                      command=window.handle_save_click),
                 call(master=window.widgets["frm_navigation"], name="btn_cancel", text="Cancel",
                      command=window.handle_cancel_click)]
        mock_button.assert_has_calls(calls)

    @patch('app.windows.messagebox.showinfo')
    @patch('app.windows.TCX_API_Connection')
    def test_handle_test_connection_success(self, mock_api, mock_messagebox_showinfo, root, mock_tcx_config):
        window = Window3cxConfig(master=root, tcx_config=mock_tcx_config)
        window.vars = {
            "scheme": MagicMock(**{'get.return_value': 'test_scheme'}),
            "domain": MagicMock(**{'get.return_value': 'test_domain'}),
            "port": MagicMock(**{'get.return_value': 'test_port'}),
            "username": MagicMock(**{'get.return_value': 'username'}),
            "password": MagicMock(**{'get.return_value': 'password'})
        }
        window.widgets["btn_test"].invoke()
        mock_api.authenticate.assert_called_once_with(
            username='username', password='password')

    def test_handle_test_connection_failure(self):
        pass

    def test_handle_cancel_click(self, window):
        with patch.object(window, 'destroy') as mock_destroy:
            window.widgets["btn_cancel"].invoke()
            mock_destroy.assert_called_once_with()

    @patch('app.windows.messagebox.showinfo')
    def test_handle_save_click_success(self, mock_messagebox_showinfo, window):
        with patch.multiple(window, write_config_file=DEFAULT, destroy=DEFAULT) as mocks:
            window.widgets["btn_save"].invoke()
            mocks["write_config_file"].assert_called_once_with()
            mock_messagebox_showinfo.assert_called_once_with(
                title='Saved!', message='Config saved!')
            mocks["destroy"].assert_called_once_with()

    @patch('app.windows.messagebox.showerror')
    def test_handle_save_click_failure(self, mock_messagebox_showerror, window):
        with patch.multiple(window, write_config_file=DEFAULT, destroy=DEFAULT) as mocks:
            mocks["write_config_file"].side_effect = ConfigSaveError
            window.widgets["btn_save"].invoke()
            mock_messagebox_showerror.assert_called_once_with(
                title='Error!', message=f"{ConfigSaveError()}")

    @patch('app.config.TCXConfig')
    def test_write_config_file_success(self, mock_tcx_config, root):
        conf = {"3cx": {
            "scheme": None,
            "domain": None,
            "port": None,
            "username": None,
            "password": None
        }}
        mock_tcx_config.__getitem__.side_effect = conf.__getitem__
        window = Window3cxConfig(master=root, tcx_config=mock_tcx_config)
        window.vars = {
            "scheme": MagicMock(**{'get.return_value': 'test_scheme'}),
            "domain": MagicMock(**{'get.return_value': 'test_domain'}),
            "port": MagicMock(**{'get.return_value': 'test_port'}),
            "username": MagicMock(**{'get.return_value': 'username'}),
            "password": MagicMock(**{'get.return_value': 'password'})
        }
        # with patch.object(window.tcx_config, 'save') as mock_tcx_config_save:
        window.write_config_file()
        mock_tcx_config.save.assert_called_once_with()

        assert mock_tcx_config["3cx"] == {
            "scheme": "test_scheme",
            "domain": "test_domain",
            "port": "test_port",
            "username": "username",
            "password": "password"
        }

    @patch('app.config.TCXConfig')
    def test_write_config_file_failure(self, mock_tcx_config, root):
        conf = {"3cx": {
            "scheme": None,
            "domain": None,
            "port": None,
            "username": None,
            "password": None
        }}
        mock_tcx_config.__getitem__.side_effect = conf.__getitem__
        mock_tcx_config.save.side_effect = Exception("An error has occurred!")
        window = Window3cxConfig(master=root, tcx_config=mock_tcx_config)
        window.vars = {
            "scheme": MagicMock(**{'get.return_value': 'test_scheme'}),
            "domain": MagicMock(**{'get.return_value': 'test_domain'}),
            "port": MagicMock(**{'get.return_value': 'test_port'}),
            "username": MagicMock(**{'get.return_value': 'username'}),
            "password": MagicMock(**{'get.return_value': 'password'})
        }
        with pytest.raises(ConfigSaveError) as e:
            window.write_config_file()

        # mock_tcx_config.__getitem__.assert_called_with("3cx")
        # mock_tcx_config.__getitem__["3cx"].assert_called_once_with()
       # mock_tcx_config.save.assert_called_once_with()
