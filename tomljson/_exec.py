# Execute the parser and write the output to the outputs folder

from pathlib import Path
from tomljson.parser._parser import _parser
from tomljson.utils._json_handle import writeJsonFile


def exec():
    input_folder = Path("./inputs")
    paths = [str(file) for file in input_folder.iterdir() if file.is_file()]
    for path in paths:
        print(f"Reading {path}")
        try:
            result = _parser(path)
            writeJsonFile(result, path.split("/")[-1].split(".")[0])
            print(f"Successfully! Outputed to the outputs folder")
        except Exception as e:
            print(f"Error: {e}")
