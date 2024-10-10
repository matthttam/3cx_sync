import os, copy, sys
from configparser import ConfigParser
from pathlib import Path
import keyring
import platformdirs


class AppConfig(ConfigParser):
    def __init__(self, *args, supress_load=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_defaults()
        self.original_config = None
        if not supress_load:
            self.load()

    @property
    def config_file_path(self) -> str:
        app_data_dir = platformdirs.user_config_dir("3cx_sync", "3cx_sync")
        config_file_path = os.path.join(app_data_dir, "conf")
        os.makedirs(config_file_path, exist_ok=True)
        return os.path.join(config_file_path, "app_conf.ini")

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

    def load_defaults(self) -> None:
        default_config = {
            "3cx": {
                "scheme": "https",
                "domain": "example.my3cx.us",
                "port": "5001",
                "username": "admin@example.com",
                "password": "password",
                "store_credential_securely": False,
            },
            "app": {"logout_hotdesk_on_disable": True},
        }
        self.read_dict(default_config)

    def load(self) -> None:
        self.read(self.config_file_path)
        if self.getboolean("3cx", "store_credential_securely"):
            self.get_credential_securely()
        self.original_config = copy.deepcopy(self)

    def save(self) -> None:
        if self.getboolean("3cx", "store_credential_securely"):
            self.save_credential_securely()
        with open(self.config_file_path, "w") as config_file:
            self.write(config_file)
        config_file.close()
        self.original_config = copy.deepcopy(self)

    def update(self, section: str, key: str, value: str):
        # Check if the section exists, if not, add it
        if not self.has_section(section):
            self.add_section(section)
        self.set(section, key, value)

    def get_credential_securely(self):
        # get credential using keyring
        password = keyring.get_password("3CX_Sync", self.get("3cx", "username"))
        self.set("3cx", "password", password)

    def save_credential_securely(self):
        # save credential using keyring
        keyring.set_password(
            "3CX_Sync", self.get("3cx", "username"), self.get("3cx", "password")
        )
        self.set("3cx", "password", None)
