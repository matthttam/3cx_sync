import os
import platformdirs


def initialize_or_get_user_config_file(app_name, app_author, folder_name, file_name):
    app_data_dir = platformdirs.user_config_dir(app_name, app_author)
    config_file_path = os.path.join(app_data_dir, folder_name)
    os.makedirs(config_file_path, exist_ok=True)
    return os.path.join(config_file_path, file_name)
