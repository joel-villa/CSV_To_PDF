"""Determines pdf layout"""

import json
from pathlib import Path
from warnings import warn

from src.ColumnSetting import ColumnSetting

DEFAULT_SETTING: str = "DEFAULT"
DEFAULT_HEADER_SIZE: int = 4
DEFAULT_PATH: Path = Path("settings/settings.json")


def get_saved_settings(
    n_cols: int = -1,
    field_names: list[str] | None = None,
) -> list[str]:
    """Get those settings which are currently saved!

    Args:
        n_cols (int): The number of columns in the csv
        field_names (list[str]): The names of the columns in th csv

    Returns:
        setting_names (list[str]): The currently saved settings

    Resources:
        - Loop through key,value of a dict:
            https://www.w3schools.com/python/python_dictionaries_loop.asp
    """
    if field_names is not None and n_cols == -1:
        n_cols = len(field_names)

    with open(DEFAULT_PATH) as f:
        json_dict = json.load(f)

    if n_cols == -1:
        # Return all setting names
        return list(json_dict.keys()[1:])  # First key is not for user to see

    setting_names = []
    for i, key in enumerate(json_dict):
        if i == 0:
            # First entry is a note to self, not an actual setting
            continue

        temp_setting = Setting(title=key)
        if temp_setting.n_cols == n_cols or n_cols == -1:
            if field_names is None:
                setting_names.append(key)
                continue
            setting_col_names = temp_setting.col_names()
            append_setting = True
            for i, set_col_name in enumerate(setting_col_names):
                if field_names[i] != set_col_name:
                    # Do not include settings with different header names
                    append_setting = False
                    continue

            if append_setting:
                # A perfect match -> save it
                setting_names.append(key)

    return setting_names


class Setting:
    """The settings object"""

    _read_only: bool
    _track_date: bool
    _title: str
    _preamble: str
    _col_order: list[int]
    _col_setting_map: dict[int, ColumnSetting]
    _PATH: Path = DEFAULT_PATH

    def __init__(
        self,
        title: str = DEFAULT_SETTING,
        read_only: bool = True,
        field_names: list[str] | None = None,
        header_size: int = DEFAULT_HEADER_SIZE,
    ) -> None:
        """Loads the setting map from the settings path

        Args:
            title (str): The title of these settings
            read_only (bool): Can these settings be updated?
            field_names (list[str]): The field names of this setting. Only
            provide these, when creating a new setting from scratch
            header_size (int): The size of the initial row
        """
        if title == DEFAULT_SETTING and read_only is False:
            raise ValueError("default setting is read only")
        if title == DEFAULT_SETTING and field_names is None:
            raise ValueError(
                "field_names must be provided for default settings (HINT: do `[str(x) for x in range(num_cols)]`)"
            )
        if field_names is not None:
            read_only = False

        self._read_only = read_only
        self._track_date = False
        self._title = title
        self._preamble = ""
        self._col_order = []
        self._col_setting_map = {}

        if field_names is None:
            # Field names of None => settings already exist load 'em
            if header_size != DEFAULT_HEADER_SIZE:
                warn(
                    f"loading results from saved settings, header_size of {header_size} is being ignored"
                )
            self.__load_settings()  # TODO make load_settings return True/False for success, upon failure, fallback to default
        else:
            # Create the default column settings!
            for col, field_name in enumerate(field_names):
                self.set_to_default(
                    column=col,
                    create_new=True,
                )
                self._col_setting_map[col].name = field_name
            self.__reset_col_order()

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
                "col_names": self.col_names(),
            }
        )

    def __check_authorization(self) -> None:
        """Check that this column setting is allowed to be written to"""
        if self._read_only:
            raise ValueError("This Setting is read only")

    def __load_settings(self) -> None:
        """Load the settings from the settings path

        Resources:
            - Json loading
                https://stackoverflow.com/questions/20199126/reading-json-from-a-file
            - Looping through a dictionary
                https://www.w3schools.com/python/python_dictionaries_loop.asp
        """
        # TODO: if setting does not exist, creating new setting
        with open(self._PATH) as f:
            json_dict = json.load(f)
            json_dict = json_dict[self._title]
            setting_dict = json_dict["col_setting_map"]

            for key, value in setting_dict.items():
                self._col_setting_map[int(key)] = ColumnSetting(
                    read_only=self._read_only, **value
                )

            self._col_order = json_dict["col_order"]
            self._preamble = json_dict["preamble"]
            self._track_date = json_dict["track_date"]

    def save_settings(self) -> None:
        """Save the settings to the settings path"""
        self.__check_authorization()
        col_map = {}

        for key, value in self._col_setting_map.items():
            col_map[key] = value.to_dict()

        this_setting_dict = {
            "col_order": self._col_order,
            "preamble": self._preamble,
            "col_setting_map": col_map,
            "track_date": self._track_date,
        }

        with open(self._PATH, "r") as json_file:
            json_dict = json.load(json_file)

        with open(self._PATH, "w") as json_file:
            json_dict[self._title] = this_setting_dict

            json.dump(json_dict, json_file, indent=4)

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

    @track_date.setter
    def track_date(self, new_val: bool) -> None:
        """A setter for track_date

        Args:
            new_val (bool): the new value for the property
        """
        self.__check_authorization()
        self._track_date = new_val

    @preamble.setter
    def preamble(self, new_val: str) -> None:
        """A setter for external_link

        Args:
            new_val (bool): the new value for the property
        """
        self.__check_authorization()
        # TODO: add markdown link formatting
        self._preamble = new_val

    def __reset_col_order(self) -> None:
        """Reset the column ordering (just increasing)

        Resources:
            - dictionary keys
                https://stackoverflow.com/questions/16819222/how-do-i-return-dictionary-keys-as-a-list-in-python
        """
        sorted_settings = list(self._col_setting_map.values())
        sorted_settings.sort()
        self._col_order = [col_setting.col_number for col_setting in sorted_settings]

    #    def swap_cols(self, col_one: int, col_two: int) -> None:
    #        """Swap the column ordering of the two columns
    #
    #        Args:
    #            col_one (int): First column to swap
    #            col_two (int): Second column to swap
    #        """
    #        self.__check_authorization()
    #        temp = self._col_order[col_one]
    #        self.col_order[col_one] = self._col_order[col_two]
    #        self.col_order[col_two] = temp

    def get_default(self, column: int) -> ColumnSetting:
        """Get the default settings for a column

        Args:
            column (int): The column to get the default settings of

        Returns:
             def_setting (ColumnSetting): The default column setting
        """
        header_number = 0
        if column == 0:
            header_number = DEFAULT_HEADER_SIZE
        return ColumnSetting(
            name=str(column),
            col_number=column,
            header_number=header_number,
            read_only=self._read_only,
        )

    def set_to_default(
        self,
        column: int,
        create_new: bool = False,
    ) -> None:
        """Set the column's settings back to default

        Args:
            column (int): The column to reset
        """
        self.__check_authorization()
        if column > self.n_cols:
            warn(
                f"Requested to create column {column}, going to create column {self.n_cols} instead"
            )
            column = self.n_cols
        self.update_setting(setting=self.get_default(column), create_new=create_new)

    def update_setting(self, setting: ColumnSetting, create_new: bool = False) -> None:
        """Update the setting for the specific column

        Args:
            column (int): The column number
            setting (ColumnSetting): The column setting
            create_new (bool): True -> allowing for new column insertion into the
            settings. False -> no such allowal. NOTE: inserting new -> setting
            default at the same time
        """
        self.__check_authorization()
        setting = ColumnSetting(read_only=self._read_only, **setting.to_dict())
        column = setting.col_number
        if self._col_setting_map.get(column) is None:
            if create_new is False:
                raise ValueError(
                    f"Cannot insert column {column} unless parameter create_new is set to True"
                )

            self._col_order.append(self.n_cols)

        self._col_setting_map[column] = setting
        self.__reset_col_order()

    #    def delete_column(self, column: int) -> None:
    #        """Delete the column from the settings
    #
    #        Args:
    #            column (int): The column to remove
    #
    #        """
    #        raise NotImplementedError

    def get_setting(self, column: int) -> ColumnSetting:
        """Get the setting for a specific column

        Args:
            column (int): The column number to get the settings for

        Returns:
             col_setting (ColumnSetting): The column settings for the column
        """
        return self._col_setting_map[column]

    def set_indicator_text(
        self,
        col: int,
        text: str | None = None,
        bolden: bool = True,
    ) -> None:
        """Set the indicator text of the given columns

        Args:
            col (int): The columns which is an indicator
            text (str): The indicator text
            bolden (bool): Is it bold?
        """
        self.__check_authorization()
        if text:
            self._col_setting_map[col].indicator_text = text
        else:
            indicator_text = self._col_setting_map[col].name
            self._col_setting_map[col].indicator_text = indicator_text.title()

        self._col_setting_map[col].is_bold = bolden

        self.__reset_col_order()

    def col_names(self) -> list[str]:
        """Get the column names of this Setting

        Returns:
            col_names (list[str]): The column names
        """
        return [value.name for value in self._col_setting_map.values()]


def main() -> None:
    """main for testing purposes"""
    default_setting = Setting(field_names=["one", "two", "three"])
    print(str(default_setting))
    for col in default_setting.col_order:
        print(f"{col}: {default_setting.get_setting(col)}")

    non_default = Setting(
        title="My Settings",
        read_only=False,
        field_names=[
            "title field",
            "other field",
            "yet another",
            "this field indicates",
        ],
    )
    print(str(non_default))
    for col in non_default.col_order:
        print(f"{col}: {non_default.get_setting(col)}")

    non_default.set_indicator_text(3, "Is Indicator Indeed")
    print(str(non_default))
    for col in non_default.col_order:
        print(f"{col}: {non_default.get_setting(col)}")

    non_default.set_indicator_text(2, "Is Indicator Indeed")
    print(str(non_default))
    for col in non_default.col_order:
        print(f"{col}: {non_default.get_setting(col)}")

    try:
        non_default.set_to_default(column=non_default.n_cols + 1)
    except ValueError as e:
        print(e)

    non_default.set_to_default(column=non_default.n_cols, create_new=True)
    print(str(non_default))
    for col in non_default.col_order:
        print(f"{col}: {non_default.get_setting(col)}")

    non_default.save_settings()

    saved_settings = Setting(title="My Settings")
    print(str(saved_settings))


if __name__ == "__main__":
    """main for testing purposes"""
    main()
