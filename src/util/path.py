from pathlib import Path

PROJECT_ROOT_DEPTH = 2


def generate_path(path: str) -> str:
    """generate the absolute path

    Args:
        path (str): Relative path from root directory.

    Returns:
        str: Absolute path
    """
    return str(Path(__file__).parents[PROJECT_ROOT_DEPTH]) + path
