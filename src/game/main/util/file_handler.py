
import json
from typing import Dict


class FileHandler:
    def __init__(self):
        pass

    @staticmethod
    def save_to(path: str, content: str) -> None:
        with open(path, "w") as f: f.write(content)

    @staticmethod
    def load_json2dict(path: str) -> Dict:
        data: Dict = dict()
        with open(path, "r") as f: data = json.load(f)
        return data

    @staticmethod
    def load_json2str(path: str) -> str:
        data: dict
        with open(path, "r") as f: data = json.load(f)
        return json.dumps(data)


if __name__ == '__main__':
    pass
