"""Determines pdf layout"""

import json
from pathlib import Path
from warnings import warn

from src.ColumnSetting import ColumnSetting


class SettingOld:
    """The settings object"""

    _read_only: bool
    _track_date: bool
    _doc_title: str
    _preamble: str
    _col_order: list[int]
    _setting_map: dict[int, ColumnSetting]
    _default_map: dict[int, ColumnSetting]
    _PATH: Path = Path("settings.json")

    def __init__(self, read_only: bool = True) -> None:
        """Loads the setting map from the settings path

        Args:
            read_only (bool): Can these settings be updated?
        """
        self._read_only = read_only
        self._track_date = False
        self._doc_title = ""
        self._preamble = ""
        self._col_order = []
        self._setting_map = {}
        self._default_map = {}
        self.__load_settings()

    def __str__(self):
        return str(
            {
                "col_order": self._col_order,
                "doc_title": self._doc_title,
                "track_date": self._track_date,
                "preamble": self._preamble,
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
        with open(self._PATH) as f:
            json_dict = json.load(f)

            default_dict = json_dict["default_map"]
            setting_dict = json_dict["setting_map"]

            for key, value in default_dict.items():
                self._default_map[int(key)] = ColumnSetting(**value)
            for key, value in setting_dict.items():
                self._setting_map[int(key)] = ColumnSetting(**value)

            self._col_order = json_dict["col_order"]
            self._doc_title = json_dict["doc_title"]
            self._preamble = json_dict["preamble"]
            self._track_date = json_dict["track_date"]

    def __save_settings(self) -> None:
        """Save the settings to the settings path"""
        #        assert type(self._default_map.values) is ColumnSetting, f"type: {type(self._default_map.values)}"
        #        assert type(self._setting_map.values) is ColumnSetting, f"type: {type(self._setting_map.values)}"

        default_dict = {}
        setting_dict = {}

        for key, value in self._default_map.items():
            default_dict[key] = value.to_dict()
        for key, value in self._setting_map.items():
            setting_dict[key] = value.to_dict()

        json_dict = {
            "col_order": self._col_order,
            "default_map": default_dict,
            "doc_title": self._doc_title,
            "preamble": self._preamble,
            "setting_map": setting_dict,
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
    def doc_title(self) -> str:
        """A getter for the document title

        Returns:
             doc_title (str): The document title
        """
        return self._doc_title

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

    @doc_title.setter
    def doc_title(self, text: str) -> None:
        """A setter for the doc_title

        Args:
            text (str): the new title
        Rsources:
            - Setter notation:
                https://realpython.com/python-property/#providing-write-only-attributes
        """
        self.__check_authorization()
        self._doc_title = text
        self.__save_settings()

    @track_date.setter
    def track_date(self, new_val: bool) -> None:
        """A setter for track_date

        Args:
            new_val (bool): the new value for the property
        """
        self.__check_authorization()
        self._track_date = new_val
        self.__save_settings()

    @preamble.setter
    def preamble(self, new_val: str) -> None:
        """A setter for external_link

        Args:
            new_val (bool): the new value for the property
        """
        self.__check_authorization()
        # TODO: add markdown link formatting
        self._preamble = new_val
        self.__save_settings()

    def reset_col_order(self) -> None:
        """Reset the column ordering (just increasing)"""
        self.__check_authorization()
        num_cols = self.n_cols
        self._col_order = list(range(num_cols))
        self.__save_settings()

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
        self.__save_settings()

    def get_default(self, column: int) -> ColumnSetting:
        """Get the default settings for a column

        Args:
            column (int): The column to get the default settings of

        Returns:
             def_setting (ColumnSetting): The default column setting
        """
        return self._default_map[column]

    def set_to_default(self, column: int) -> None:
        """Set the column's settings back to default

        Args:
            column (int): The column to reset
        """
        self.__check_authorization()
        self._setting_map[column] = self.get_default(column)
        self.__save_settings()

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
        if self._setting_map.get(column) is None:
            if create_new is False:
                raise ValueError(
                    f"Cannot insert column {column} unless parameter create_new is set to True"
                )

            self._col_order.append(self.n_cols)
            # Creating new column setting, spooky
            warn(
                f"Column {column}, is not currently in settings, adding it is also setting as default."
            )
            self._default_map[column] = setting

        self._setting_map[column] = setting
        self.__save_settings()

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
        return self._setting_map[column]


def test_setting(setting: SettingOld) -> None:
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
        setting.doc_title = "A Terrible Tittle"
    except ValueError:
        num_exceptions += 1

    print(f"Title: {setting.doc_title}")

    possible_exceptions += 1
    try:
        setting.preamble = "A terrifying preamble"
    except ValueError:
        num_exceptions += 1

    print(f"Preamble: {setting.preamble}")

    print(f"num_exceptions: {num_exceptions} out of {possible_exceptions}")


def main() -> None:
    """main for testing purposes"""
    setting = SettingOld(read_only=False)
    test_setting(setting)
    immutable_setting = SettingOld()
    test_setting(immutable_setting)


if __name__ == "__main__":
    """main for testing purposes"""
    main()
