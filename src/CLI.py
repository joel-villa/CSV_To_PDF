"""The Interface for interacting with the user"""

# NOTE: should be useable without CLI: just put .pdf in same location as csv (do not override anything existing)

import csv
from pathlib import Path

from src.Setting import Setting, get_saved_settings


class CLI:
    """The Command Line Interface"""

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

    def __create_new_setting(self, column_names: list[str]) -> str:
        """Create a new setting via user input

        Args:
            column_names (list[str]): The column names

        Returns:
            setting_title (str): Title of the created and saved setting
        """
        title = input(
            "\nCreating new setting!\nEnter the title of the document (will be both the pdf header + what this setting gets saved as):\n"
        )
        setting = Setting(
            title=title,
            read_only=False,
            field_names=column_names,
        )

        # To save the date or not to save the date, that is the question
        track_date = input(
            "\nDisplay the Month & year the pdf was created? [y]es/[n]o: "
        )
        if track_date.lower() in {"y", "yes"}:
            print("Tracking the pdf creation date")
            setting.track_date = True
        else:
            if track_date.lower() not in {"n", "no"}:
                print(f"Defaulting to not saving the date, invalid input: {track_date}")
            else:
                print("Not tracking the pdf creation date")
            setting.track_date = False

        has_preamble = input(
            "\nAny additional text to display (e.g. 'for the defacto list of resources see...')? [y]es, [n]o: "
        )

        if has_preamble.lower() in {"y", "yes"}:
            setting.preamble = input("Please type the preamble and hit enter:\n")
        elif has_preamble.lower() not in {"n", "no"}:
            print(f"Defaulting to no preamble, invalid input: {track_date}")

        # Last but not least, determine if there are indicators (more complexity here)
        has_indicators = input(
            "\nAny indicator fields, default is no (e.g. 'Faith-based')? [y]es/[n]o: "
        )
        if has_indicators.lower() in {"y", "yes"}:
            print("Columns:")
            for (
                i,
                col_name,
            ) in enumerate(column_names):
                print(f"{i + 1}. {col_name}")

            done = False
            while not done:
                col_name = input(
                    "Type the column number which is true/false OR 'q' to stop: "
                )
                if col_name == "q":
                    break
                try:
                    col_idx = int(col_name) - 1
                    if col_idx >= 0 and col_idx < len(column_names):
                        print(
                            f"column {column_names[col_idx]} is set to an indicator column"
                        )
                        setting.set_indicator_text(col_idx)
                        continue

                except ValueError:
                    pass
                if col_name not in column_names:
                    print(f"Invalid column choice: {col_name}")
                else:
                    print(
                        f"God I'm good...\tcolumn {col_name} is set to an indicator column"
                    )
                    setting.set_indicator_text(column_names.index(col_name))
        elif has_indicators.lower() not in {"n", "no"}:
            print(f"Defaulting to no indicators, invalid input: {has_indicators}")

        print(f"Saving Setting: {setting}")
        setting.save_settings()
        return title

    def run(self) -> tuple[Path, Path, str | None]:
        """Do all that user interaction goodness

        Args:
            name (type): Description

        Returns:
             csv_path (Path): The path to the csv file
             pdf_path (Path): The path to the pdf file
             setting_name (str): The name of the setting to load

        Resources:
            - User CLI input:
                https://stackoverflow.com/questions/70797/user-input-and-command-line-arguments
            - Checking path validity:
                https://www.geeksforgeeks.org/python/check-if-a-file-exists-in-python/
            - Path suffixes & file creation:
                https://docs.python.org/3/library/pathlib.html
            - Python strings are immutable...
                https://stackoverflow.com/questions/2165172/replacing-one-character-of-a-string-in-python
            - next() function for itterating an iterable:
                https://stackoverflow.com/questions/17262256/how-to-read-one-single-line-of-csv-data-in-python
            - Index of an item in a list:
                https://www.geeksforgeeks.org/python/python-list-index/
        """
        # TODO: going back with 'q'
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

        with open(csv_path) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",", quotechar='"')
            column_names = next(spamreader)

        valid_settings = get_saved_settings(field_names=column_names)
        chosen_setting = None

        print("\nSetting Options:")
        print("0. This is a DEFAULT option")
        i = 0
        while i < len(valid_settings):
            print(f"{i + 1}. {valid_settings[i]}")
            i += 1
        print(f"{i + 1}. Choose this option to CREATE A NEW SETTING")
        choice = input(
            "Select one of the above settings by typing its corresponding number: "
        )

        try:
            choice = int(choice) - 1
        except ValueError:
            if choice.lower() == "anything else":
                print("...\n...\n...\nHow polite\n\t=]")
            choice = -2

        if choice in range(len(valid_settings)):
            chosen_setting = valid_settings[choice]
        elif choice != -1:
            chosen_setting = self.__create_new_setting(column_names=column_names)
        else:
            chosen_setting = None

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

        return csv_path, pdf_path, chosen_setting


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
