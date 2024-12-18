import json
from abc import ABC, abstractmethod

class StorageHandler(ABC):
    @abstractmethod
    def save_product(self, product_data):
        pass

class JSONFileStorage(StorageHandler):
    def __init__(self, file_path):
        self.file_path = file_path

    def save_product(self, product_data):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(product_data)

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
