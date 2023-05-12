import sys
from pathlib import Path

def initPackage() -> bool:
    try:
        sys.path.append(str(Path(__file__).parent) + "/tomljson")
    except Exception as e:
        print(f"Error: {e}")
        return False
    return True


def main():
    sucess = initPackage()
    if sucess:
        from tomljson._exec import exec
        exec()
    else:
        print("Error: Failed to initialize the package")


if __name__ == "__main__":
    main()