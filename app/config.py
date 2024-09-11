import os
from configparser import ConfigParser


class AppConfig(ConfigParser):
    @property
    def defaults_config_file_path(self) -> str:
        return os.path.join(os.getcwd(), "conf", "app_defaults.ini")

    @property
    def config_file_path(self) -> str:
        return os.path.join(os.getcwd(), "conf", "app_conf.ini")

    @property
    def server_url(self) -> str:
        return (
            self["3cx"].get("scheme")
            + "://"
            + self["3cx"].get("domain")
            + ":"
            + self["3cx"].get("port")
        )

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def load(self) -> None:
        self.read([self.defaults_config_file_path, self.config_file_path])

    def save(self) -> None:
        with open(self.config_file_path, "w") as config_file:
            self.write(config_file)
        config_file.close()


# class AppConfig(ConfigParser):
#    @property
#    def defaults_config_file_path(self):
#        return os.path.join(os.getcwd(), "conf", "defaults.ini")
#
#    @property
#    def config_file_path(self):
#        return os.path.join(os.getcwd(), "conf", "app_conf.ini")
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(self, *args, **kwargs)
#        self.read([self.defaults_config_file_path, self.config_file_path])
