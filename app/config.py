import os, copy, sys
from configparser import ConfigParser
from pathlib import Path


class AppConfig(ConfigParser):
    def __init__(self, *args, supress_load=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_config = None
        if not supress_load:
            self.load()

    def get_config_path(self) -> str:
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            conf_path = Path(sys._MEIPASS)
        else:
            conf_path = os.path.join(os.getcwd(), "conf")
        return conf_path

    @property
    def defaults_config_file_path(self) -> str:

        return os.path.join(self.get_config_path(), "app_defaults.ini")

    @property
    def config_file_path(self) -> str:
        return os.path.join(self.get_config_path(), "app_conf.ini")

    @property
    def server_url(self) -> str:
        return (
            self["3cx"].get("scheme")
            + "://"
            + self["3cx"].get("domain")
            + ":"
            + self["3cx"].get("port")
        )

    @property
    def is_dirty(self) -> bool:
        return self.original_config != self

    def load(self) -> None:
        self.read([self.defaults_config_file_path, self.config_file_path])
        self.original_config = copy.deepcopy(self)

    def save(self) -> None:
        with open(self.config_file_path, "w") as config_file:
            self.write(config_file)
        config_file.close()
        self.original_config = copy.deepcopy(self)

    def update(self, section: str, key: str, value: str):
        # Check if the section exists, if not, add it
        if not self.has_section(section):
            self.add_section(section)
        self.set(section, key, value)
