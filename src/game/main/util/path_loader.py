
# import importlib.resources as rsrc
from pathlib import Path
import src


def get_absolute_resource_path(path: str) -> str:
    # resources_absolute_path: str = str(rsrc.path("src", ""))
    # return resources_absolute_path + "\\game\\resources" + path
    return str(Path(src.__file__).parent) + "\\game\\resources" + path


if __name__ == '__main__':
    pass
