"""Determines pdf layout"""


import json
from pathlib import Path
from warnings import warn

from src.ColumnSetting import ColumnSetting


class Settings:
    """The settings object"""

    _read_only: bool
    _setting_map: dict[int, ColumnSetting]
    _default_map: dict[int, ColumnSetting]
    _col_order: list[int]
    _doc_title: str
    _track_date: bool
    _external_link: str
    _PATH: Path = Path("settings/settings.json")

    def __init__(self, read_only: bool = True) -> None:
        """Loads the setting map from the settings path

        Args:
            read_only (bool): Can these settings be updated?
	    """
        self._read_only = read_only
        self._setting_map = {}
        self._default_map = {}
        self._doc_title = ""
        self._col_order = []
        self._doc_title = ""
        self._track_date = False
        self._external_link = ""
        self.__load_settings()


    def __load_settings(self) -> None:
        """Load the settings from the settings path

        Resources:
            - Json loading
                https://stackoverflow.com/questions/20199126/reading-json-from-a-file
            - Looping through a dictionary
                https://www.w3schools.com/python/python_dictionaries_loop.asp
        """
        raise NotImplementedError
        with open(self._PATH) as f:
            setting_dict = json.load(f)

            #TODO: finish settings reading + writing implementation
            self._col_order = setting_dict['col_order']
            self._doc_title = setting_dict['doc_title']

            self._title_font = Font(**setting_dict['title_font'])

            setting_map = setting_dict['setting_map']
            default_map = setting_dict['default_map']

            for json_map, self_map in zip([setting_map, default_map], [self._setting_map, self._default_map]):
                for key, value in json_map.items():
                    font = Font(**value['font'])
                    self_map[int(key)] = ColumnSetting(
                        font=font,
                        is_indicator=value['is_indicator'],
                        additional_text=value['additional_text'],
                    )

    def __save_settings(self) -> None:
        """Save the settings to the settings path"""
        raise NotImplementedError
        setting_map = {}
        default_map = {}
        for json_map, self_map in zip([setting_map, default_map], [self._setting_map, self._default_map]):
            for key, value in self_map.items():
                json_map[key] = value.to_dict()

        json_dict = {}
        json_dict['col_order'] = self._col_order
        json_dict['doc_title'] = self._doc_title
        json_dict['title_font'] = self.title_font.to_dict()
        json_dict['setting_map'] = setting_map
        json_dict['default_map'] = default_map

        with open(self._PATH, "w") as json_file:
            json.dump(json_dict, json_file, indent=4)

    def __check_authorization(self) -> None:
        """Check that this column setting is allowed to be written to"""
        if self._read_only:
            raise ValueError("This Column Setting is read only")

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
    def external_link(self) -> str:
        """A getter for external_link

        Returns:
             track_date (bool): The link to the external website
	   """
        return self._external_link

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

    @external_link.setter
    def external_link(self, new_val: str) -> None:
        """A setter for external_link

        Args:
            new_val (bool): the new value for the property
        """
        self.__check_authorization()
        self._external_link = new_val
        self.__save_settings()

    def reset_col_order(self) -> None:
        """Reset the column ordering (just increasing)"""
        self.__check_authorization()
        num_cols = len(self.col_order)
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
        self,
        column: int,
        setting: ColumnSetting,
        create_new: bool = False
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
                raise ValueError(f"Cannot insert column {column} unless parameter create_new is set to True")

            num_cols = len(self.col_order)
            self._col_order.append(num_cols)
            # Creating new column setting, spooky
            warn(f"Column {column}, is not currently in settings, adding it is also setting as default.")
            self._default_map[column] = setting

        self._setting_map[column] = setting
        self.__save_settings()


    def get_setting(self, column: int) -> ColumnSetting:
        """Get the setting for a specific column

        Args:
            column (int): The column number to get the settings for

        Returns:
             col_setting (ColumnSetting): The column settings for the column
	    """
        return self._setting_map[column]
