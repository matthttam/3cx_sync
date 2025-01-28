import code

from app.config import AppConfig
from threecxapi.connection import ThreeCXApiConnection

from threecxapi.resources.users import *
from threecxapi.resources.groups import *
from threecxapi.resources.peers import *
from threecxapi.resources.trunks import *


def load_config():
    print("Loading configuration...")
    app_config = AppConfig()
    app_config.load()
    return app_config


def authenticate_to_api(config):
    api_connection = ThreeCXApiConnection(server_url=config.server_url)
    api_connection.authenticate(
        username=config["3cx"].get("username"),
        password=config["3cx"].get("password"),
    )
    return api_connection


config = load_config()
api_connection = authenticate_to_api(config)

# Prepare the global environment for the interactive shell
globals_ = globals().copy()
globals_["config"] = config  # Making the config available
globals_["api_connection"] = api_connection  # Making the API response available


# Drop into an interactive Python shell
def start_shell():
    print("\nInteractive shell starting. Type 'exit()' to quit.")
    shell = code.InteractiveConsole(globals_)
    shell.interact(banner="Welcome to the interactive shell!")


# Run the interactive shell
if __name__ == "__main__":
    trunks_resource = TrunksResource(api=api_connection)
    original_trunk_id = 151
    test_trunk_id = 3886
    get_params = GetTrunkParameters()
    test_trunk = trunks_resource.get_trunk(test_trunk_id, get_params)
    original_trunk = trunks_resource.get_trunk(original_trunk_id, get_params)
    print("Test Trunk:\r\n")
    print(test_trunk.model_dump())
    print("Original Trunk:\r\n")
    print(original_trunk.model_dump())
    start_shell()
