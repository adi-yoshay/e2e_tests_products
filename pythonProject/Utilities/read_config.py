import os
import json


class AppConfiguration:
    CONFIG_FILE_PATH = os.path.abspath("../config.json")

    @staticmethod
    def get_app_configuration():
        """
        Reads the config.json file.
        Tries to read from the current directory first, then from the absolute path.
        """
        try:
            # Attempt to read from the current directory
            config_data = AppConfiguration.read_file("config.json")
        except FileNotFoundError:
            # If not found, attempt to read from the absolute path
            config_file_path = AppConfiguration.CONFIG_FILE_PATH
            config_data = AppConfiguration.read_file(config_file_path)

        return config_data

    @staticmethod
    def get_common_info():
        """
        Retrieves common information from the configuration data.
        """
        config_data = AppConfiguration.get_app_configuration()
        config_common_data = config_data["common info"]
        return config_common_data

    @staticmethod
    def read_file(file_name):
        # Get the absolute path to the config file
        base_path = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_path, "..", file_name)
        full_path = os.path.abspath(full_path)

        with open(full_path, 'r') as f:
            return json.load(f)
