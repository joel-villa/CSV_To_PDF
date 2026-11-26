"""The Interface for interacting with the user"""

# NOTE: should be useable without CLI: just put .pdf in same location as csv (do not override anything existing)

from pathlib import Path

from src.SettingOld import SettingOld


class CLI:
    """The Command Line Interface"""

    _settings: SettingOld
    _QUERY_LIST = (
        "Paste the path to the .csv file:\n",
        "Paste the path to the .csv file:\n",
        "csv please:\n",
        "do the dang thang:\n",
        "I hope you're having a good day:\n",
        "Paste the path to the .csv file:\n",
        "If you were a csv, would you dream of being a pdf:\n",
        "Paste the path to the .csv file:\n",
        "Paste the path to the .csv file:\n",
        "Paste the path to the .csv file:\n",
        "=^..^=:\n",
    )

    def __init__(
        self,
    ) -> None:
        """Construct that CLI ASAP"""
        self._settings = SettingOld(read_only=False)

    def run(self) -> tuple[Path, Path]:
        """Do all that user interaction goodness

        Args:
            name (type): Description

        Returns:
             csv_path (Path): The path to the csv file
             pdf_path (Path): The path to the pdf file

        Resources:
            - User CLI input:
                https://stackoverflow.com/questions/70797/user-input-and-command-line-arguments
            - Checking path validity:
                https://www.geeksforgeeks.org/python/check-if-a-file-exists-in-python/
            - Path suffixes & file creation:
                https://docs.python.org/3/library/pathlib.html
            - Python strings are immutable...
                https://stackoverflow.com/questions/2165172/replacing-one-character-of-a-string-in-python
        """
        csv_path: Path
        pdf_path: Path
        str_path: str
        i = 0

        while True:
            str_path = input(self._QUERY_LIST[i])
            csv_path = Path(str_path)
            if (csv_path.exists()) and (csv_path.suffix == ".csv"):
                break

            print(f'Invalid path: "{str_path}"\n')
            i += 1
            i %= len(self._QUERY_LIST)

        num_copies = 0
        num_chars = 0

        while True:
            # Handle multiple copies
            match num_copies:
                case 0:
                    str_path = f"{str_path[:-4]}.pdf"
                case 1:
                    str_path = f"{str_path[:-4]} ({num_copies}).pdf"
                    num_chars = 1
                case _:
                    str_path = f"{str_path[: -(7 + num_chars)]} ({num_copies}).pdf"
                    num_chars = len(str(num_copies))

            pdf_path = Path(str_path)
            if not pdf_path.exists():
                break

            num_copies += 1

        pdf_path.touch()

        return csv_path, pdf_path


def main() -> None:
    """main for testing purposes"""

    cli = CLI()
    for i in range(4):
        path = cli.run()
        print(f"{i}: {path}")


if __name__ == "__main__":
    """main for testing purposes

    Resources:
        - Main:
            https://docs.python.org/3/library/__main__.html
    """
    main()
