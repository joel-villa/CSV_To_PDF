"""Determines pdf layout"""

import json
from pathlib import Path
from warnings import warn

from src.ColumnSetting import ColumnSetting


class Setting:
    """The settings object"""

    _read_only: bool
    _track_date: bool
    _title: str
    _preamble: str
    _col_order: list[int]
    _col_setting_map: dict[int, ColumnSetting]
    _PATH: Path = Path("settings/settings.json")

    def __init__(self, title: str = "default", read_only: bool = True) -> None:
        """Loads the setting map from the settings path

        Args:
            read_only (bool): Can these settings be updated?
        """
        if (title == "default" and read_only is False):
            raise ValueError("default setting is read only")
        self._read_only = read_only
        self._track_date = False
        self._title = title
        self._preamble = ""
        self._col_order = []
        self._col_setting_map = {}
        self.__load_settings()

    def __str__(self) -> str:
        """To string!

        Returns:
            setting_str (str): String represesntation of the settings
	    """
        return str(
            {
                "title": self._title,
                "read_only": self._read_only,
                "track_date": self._track_date,
                "preamble": self._preamble,
                "col_order": self._col_order,
            }
        )

    def __load_settings(self) -> None:
        """Load the settings from the settings path

        Resources:
            - Json loading
                https://stackoverflow.com/questions/20199126/reading-json-from-a-file
            - Looping through a dictionary
                https://www.w3schools.com/python/python_dictionaries_loop.asp
        """
        #TODO: if setting does not exist, creating new setting
        with open(self._PATH) as f:
            json_dict = json.load(f)
            json_dict = json_dict[self._title]
            setting_dict = json_dict["col_setting_map"]

            for key, value in setting_dict.items():
                self._col_setting_map[int(key)] = ColumnSetting(**value)

            self._col_order = json_dict["col_order"]
            self._preamble = json_dict["preamble"]
            self._track_date = json_dict["track_date"]

    def save_settings(self) -> None:
        """Save the settings to the settings path"""
        self.__check_authorization()
        setting_dict = {}

        for key, value in self._col_setting_map.items():
            setting_dict[key] = value.to_dict()

        json_dict = {
            "col_order": self._col_order,
            "preamble": self._preamble,
            "col_setting_map": setting_dict,
            "track_date": self._track_date,
        }

        with open(self._PATH, "w") as json_file:
            json.dump(json_dict, json_file, indent=4)

    def __check_authorization(self) -> None:
        """Check that this column setting is allowed to be written to"""
        if self._read_only:
            raise ValueError("This Setting is read only")

    @property
    def read_only(self) -> bool:
        """A getter for read_only

        Returns:
             read_only (bool): Can these settings be updated?
        """
        return self._read_only

    @property
    def n_cols(self) -> int:
        """A getter for n_cols

        Returns:
             n_cols (int): The number of columns
        """
        return len(self.col_order)

    @property
    def col_order(self) -> list[int]:
        """A getter for the col_order

        Returns:
             col_order (list[int]): The ordering of the columns
        """
        return self._col_order

    @property
    def title(self) -> str:
        """A getter for the document title

        Returns:
             doc_title (str): The document title
        """
        return self._title

    @property
    def track_date(self) -> bool:
        """A getter for track_date

        Returns:
             track_date (bool): track the date?
        """
        return self._track_date

    @property
    def preamble(self) -> str:
        """A getter for external_link

        Returns:
             preamble (str): Some extra functionality
        """
        return self._preamble

    @title.setter
    def title(self, text: str) -> None:
        """A setter for the doc_title

        Args:
            text (str): the new title
        Rsources:
            - Setter notation:
                https://realpython.com/python-property/#providing-write-only-attributes
        """
        self.__check_authorization()
        self._title = text
        self.save_settings()

    @track_date.setter
    def track_date(self, new_val: bool) -> None:
        """A setter for track_date

        Args:
            new_val (bool): the new value for the property
        """
        self.__check_authorization()
        self._track_date = new_val
        self.save_settings()

    @preamble.setter
    def preamble(self, new_val: str) -> None:
        """A setter for external_link

        Args:
            new_val (bool): the new value for the property
        """
        self.__check_authorization()
        # TODO: add markdown link formatting
        self._preamble = new_val
        self.save_settings()

    def reset_col_order(self) -> None:
        """Reset the column ordering (just increasing)"""
        self.__check_authorization()
        num_cols = self.n_cols
        self._col_order = list(range(num_cols))
        self.save_settings()

    def swap_cols(self, col_one: int, col_two: int) -> None:
        """Swap the column ordering of the two columns

        Args:
            col_one (int): First column to swap
            col_two (int): Second column to swap
        """
        self.__check_authorization()
        temp = self._col_order[col_one]
        self.col_order[col_one] = self._col_order[col_two]
        self.col_order[col_two] = temp
        self.save_settings()

    def update_setting(
        self, column: int, setting: ColumnSetting, create_new: bool = False
    ) -> None:
        """Update the setting for the specific column

        Args:
            column (int): The column number
            setting (ColumnSetting): The column setting
            create_new (bool): True -> allowing for new column insertion into the
            settings. False -> no such allowal. NOTE: inserting new -> setting
            default at the same time
        """
        self.__check_authorization()
        if self._col_setting_map.get(column) is None:
            if create_new is False:
                raise ValueError(
                    f"Cannot insert column {column} unless parameter create_new is set to True"
                )

            self._col_order.append(self.n_cols)

        self._col_setting_map[column] = setting
        self.save_settings()

    def delete_column(self, column: int) -> None:
        """Delete the column from the settings

        Args:
            column (int): The column to remove

        """
        raise NotImplementedError

    def get_setting(self, column: int) -> ColumnSetting:
        """Get the setting for a specific column

        Args:
            column (int): The column number to get the settings for

        Returns:
             col_setting (ColumnSetting): The column settings for the column
        """
        return self._col_setting_map[column]

    def

    def set_indicator_text(
        self,
        cols: list[int],
        text: list[str],
    ) -> None:
        """Set the indicator text of the given columns

        Args:
            cols (list[int]): The columns which are indicators
            text (list[str]): The indicator text
    	"""
        self.__check_authorization()
        for i, col in enumerate(cols):
            if i < len(text):
                self._col_setting_map[col].indicator_text = text[i]
            else:

        if


def test_setting(setting: Setting) -> None:
    """For testing purposes

    Args:
        setting (Setting): the setting to test
    """
    num_cols = 7
    default_setting = ColumnSetting()
    num_exceptions = 0
    possible_exceptions = 0

    possible_exceptions += 1
    try:
        for i in range(num_cols):
            setting.update_setting(column=i, setting=default_setting, create_new=True)
    except ValueError:
        num_exceptions += 1

    for i in range(num_cols):
        col_setting = setting.get_setting(i)
        print(f"col_setting {i}: {col_setting}")

    possible_exceptions += 1
    try:
        setting.update_setting(
            column=0,
            setting=ColumnSetting(read_only=True, indicator_text="Just messing around"),
        )
    except ValueError:
        num_exceptions += 1

    print(f"col_setting 0: {setting.get_setting(0)}")

    possible_exceptions += 1
    try:
        setting.set_to_default(0)
    except ValueError:
        num_exceptions += 1

    print(f"col_setting 0: {setting.get_setting(0)}")

    print(f"col_order: {setting.col_order}")

    possible_exceptions += 1
    try:
        setting.swap_cols(
            col_one=0,
            col_two=1,
        )
    except ValueError:
        num_exceptions += 1

    print(f"col_order: {setting.col_order}")

    possible_exceptions += 1
    try:
        setting.reset_col_order()
    except ValueError:
        num_exceptions += 1

    print(f"col_order: {setting.col_order}")

    possible_exceptions += 1
    try:
        setting.title = "A Terrible Tittle"
    except ValueError:
        num_exceptions += 1

    print(f"Title: {setting.title}")

    possible_exceptions += 1
    try:
        setting.preamble = "A terrifying preamble"
    except ValueError:
        num_exceptions += 1

    print(f"Preamble: {setting.preamble}")

    print(f"num_exceptions: {num_exceptions} out of {possible_exceptions}")


def main() -> None:
    """main for testing purposes"""
    setting = Setting(read_only=False)
    test_setting(setting)
    immutable_setting = Setting()
    test_setting(immutable_setting)


if __name__ == "__main__":
    """main for testing purposes"""
    main()
