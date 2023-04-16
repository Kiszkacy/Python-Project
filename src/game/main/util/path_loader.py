
import importlib.resources as rsrc


def get_absolute_resource_path(path: str) -> str:
    resources_absolute_path: str = str(rsrc.path("src", ""))
    return resources_absolute_path + "\\game\\resources" + path


if __name__ == '__main__':
    pass
