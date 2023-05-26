# Read file


def handlePath(filepath: str):
    return filepath.split("/")


def readFile(filepath: str):
    with open(filepath, "r") as file:
        return file.read()
