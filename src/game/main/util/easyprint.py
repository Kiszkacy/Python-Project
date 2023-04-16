
class Color:
    CLEAR = "\033[m"
    DEFAULT = "\033[m"

    WEAK_BLACK = "\033[90m"
    WEAK_RED = "\033[31m"
    WEAK_GREEN = "\033[32m"
    WEAK_YELLOW = "\033[33m"
    WEAK_BLUE = "\033[34m"
    WEAK_VIOLET = "\033[35m"
    WEAK_CYAN = "\033[36m"

    BLACK = "\033[30m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    VIOLET = "\033[95m"
    CYAN = "\033[96m"

    GRAY = "\033[37m"
    WHITE = "\033[97m"


def pcol(col: Color, *args, end: str = "\n", sep: str = " ") -> None:
    print(col, end="")
    print(*args, end="", sep=sep)
    print(Color.CLEAR, end=end)


def ccol() -> None:
    print(Color.CLEAR, end="")


def scol(col: Color) -> None:
    print(col, end="")


if __name__ == '__main__':
    pass