import keyring
from copy import deepcopy
from configparser import ConfigParser
from app.util import initialize_or_get_user_config_file


class AppConfig(ConfigParser):
    def __init__(self, *args, supress_load=False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.original_config = None
        self.default_config = {
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
        return initialize_or_get_user_config_file("3cx_sync", "3cx_sync", "conf", "app_conf.ini")

    @property
    def is_dirty(self) -> bool:
        return self.original_config != self

    @property
    def store_credential_securely(self) -> bool:
        return self.getboolean("3cx", "store_credential_securely")

    def load_defaults(self) -> None:
        self.read_dict(self.default_config)

    def load(self) -> None:
        self.read(self.config_file_path)
        self.fetch_secure_credential()
        self.set_original_config()

    def save(self) -> None:
        self.store_secure_credential()
        with open(self.config_file_path, "w") as config_file:
            self.write(config_file)
        self.set_original_config()

    def set_original_config(self):
        self.original_config = deepcopy(self)

    def set_value(self, section: str, key: str, value: str):
        if not self.has_section(section):
            self.add_section(section)
        self.set(section, key, value)

    def fetch_secure_credential(self):
        # If not set to store credential securely, return
        if not self.store_credential_securely:
            return
        # get credential using keyring
        password = keyring.get_password("3CX_Sync", self.get("3cx", "username"))
        self.set("3cx", "password", password)

    def store_secure_credential(self):
        # If not set to store credential securely, return
        if not self.store_credential_securely:
            return
        # save credential using keyring
        keyring.set_password(
            "3CX_Sync", self.get("3cx", "username"), self.get("3cx", "password")
        )
        self.set("3cx", "password", None)
