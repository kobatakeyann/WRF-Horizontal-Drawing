from pathlib import Path


def generate_path(path: str) -> str:
    """絶対パスを生成

    Arg:
      path (str): rootからの相対パス

    Return:
      str: 引数pathへの絶対パス
    """
    return str(Path(__file__).parents[2]) + path
