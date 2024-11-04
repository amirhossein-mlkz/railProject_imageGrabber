import json
import os

class manifestLoader:

    def __init__(self, path) -> None:
        self.path = path
        self.manifest_data = {}
        self.load()

    def load(self,):
        if os.path.exists(self.path):
            with open(self.path, "r") as manifest_file:
                self.manifest_data = json.load(manifest_file)
                return True
        return False

    def get_version(self,):
        return self.manifest_data.get('version', -1)

    