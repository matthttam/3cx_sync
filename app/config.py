import os, copy, sys
from configparser import ConfigParser
from pathlib import Path
import keyring
import platformdirs


class AppConfig(ConfigParser):
    def __init__(self, *args, supress_load=False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.original_config = None
        if not supress_load:
            self.load_defaults()
            self.load()

    @property
    def server_url(self) -> str:
        scheme = self["3cx"].get("scheme")
        domain = self["3cx"].get("domain")
        port = self["3cx"].get("port")

        return f"{scheme}://{domain}:{port}"

    @property
    def config_file_path(self) -> str:
        app_data_dir = platformdirs.user_config_dir("3cx_sync", "3cx_sync")
        config_file_path = os.path.join(app_data_dir, "conf")
        os.makedirs(config_file_path, exist_ok=True)
        return os.path.join(config_file_path, "app_conf.ini")

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
            self.fetch_secure_credential()
        self.original_config = copy.deepcopy(self)

    def save(self) -> None:
        if self.getboolean("3cx", "store_credential_securely"):
            self.store_secure_credential()
        with open(self.config_file_path, "w") as config_file:
            self.write(config_file)
        self.original_config = copy.deepcopy(self)

    def set_value(self, section: str, key: str, value: str):
        if not self.has_section(section):
            self.add_section(section)
        self.set(section, key, value)

    def fetch_secure_credential(self):
        # get credential using keyring
        password = keyring.get_password("3CX_Sync", self.get("3cx", "username"))
        self.set("3cx", "password", password)

    def store_secure_credential(self):
        # save credential using keyring
        keyring.set_password(
            "3CX_Sync", self.get("3cx", "username"), self.get("3cx", "password")
        )
        self.set("3cx", "password", None)
