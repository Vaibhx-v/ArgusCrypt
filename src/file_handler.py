from pathlib import Path


def read_file(file_path):
    """
    Reads a file in binary mode.
    Returns:
        data (bytes)
        path (Path)
    """

    path = Path(file_path)

    with open(path, "rb") as file:
        data = file.read()

    return data, path


def write_file(file_path, data):
    """
    Writes binary data to a file.
    """

    path = Path(file_path)

    # Create parent folders if they don't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "wb") as file:
        file.write(data)