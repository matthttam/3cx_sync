import os
from configparser import ConfigParser


class TCXConfig(ConfigParser):
    @property
    def defaults_config_file_path(self):
        return os.path.join(os.getcwd(), "conf", "3cx_defaults.ini")

    @property
    def config_file_path(self):
        return os.path.join(os.getcwd(), "conf", "3cx_conf.ini")

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.read_config_files()

    def read_config_files(self):
        self.read([self.defaults_config_file_path, self.config_file_path])

    def get_server_url(self):
        return (
            self["3cx"].get("scheme")
            + "://"
            + self["3cx"].get("domain")
            + ":"
            + self["3cx"].get("port")
        )


class AppConfig(ConfigParser):
    @property
    def defaults_config_file_path(self):
        return os.path.join(os.getcwd(), "conf", "defaults.ini")

    @property
    def config_file_path(self):
        return os.path.join(os.getcwd(), "conf", "app_conf.ini")

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.read([self.defaults_config_file_path, self.config_file_path])
