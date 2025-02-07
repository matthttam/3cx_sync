import os
import platformdirs
from pathlib import Path


def initialize_or_get_user_config_path(app_name, app_author, folder_name) -> Path:
    app_data_dir = platformdirs.user_config_dir(app_name, app_author)
    config_file_path = os.path.join(app_data_dir, folder_name)
    os.makedirs(config_file_path, exist_ok=True)
    return Path(config_file_path)
