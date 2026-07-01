from pathlib import Path


def read_file(file_path):
    """
    Reads any file in binary mode.
    Returns:
        data (bytes)
        path (Path object)
    """

    path = Path(file_path)

    with open(path, "rb") as file:
        data = file.read()

    return data, path