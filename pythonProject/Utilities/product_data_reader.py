import json
import os

class ProductDataReader:
    @staticmethod
    def get_products_to_add():
        file_path = os.path.join(os.path.dirname(__file__), "..", "data", "products.json")
        with open(os.path.abspath(file_path)) as f:
            return json.load(f)["products_to_add"]
