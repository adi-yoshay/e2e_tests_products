import json
import os

class UserDataReader:
    @staticmethod
    def get_user_credentials(user_type: str):
        data_file = os.path.join(os.path.dirname(__file__), "../data/users.json")
        with open(data_file) as f:
            users = json.load(f)
        return users[user_type]
