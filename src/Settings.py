"""Settings, ooh, how profesional"""

import json
from pathlib import Path
from warnings import warn

from src.ColumnSetting import ColumnSetting
from src.Font import Font


class Settings:
    """The settings object"""

    _setting_map: dict[int, ColumnSetting]
    _default_map: dict[int, ColumnSetting]
    _doc_title: str
    _col_order: list[int]
    _PATH: Path = Path("settings/settings.json")

    def __init__(self) -> None:
        """Loads the setting map from the settings path
	    """
        self._setting_map = {}
        self._default_map = {}
        self._col_order = []
        self._doc_title = ""
        self.__load_settings()


    def __load_settings(self) -> None:
        """Load the settings from the settings path

        Resources:
            - Json loading
                https://stackoverflow.com/questions/20199126/reading-json-from-a-file
            - Looping through a dictionary
                https://www.w3schools.com/python/python_dictionaries_loop.asp
        """
        with open(self._PATH) as f:
            setting_dict = json.load(f)

            #TODO: finish settings reading + writing implementation
            self._col_order = setting_dict['col_order']
            self._doc_title = setting_dict['doc_title']

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
        setting_map = {}
        default_map = {}
        for json_map, self_map in zip([setting_map, default_map], [self._setting_map, self._default_map]):
            for key, value in self_map.items():
                json_map[key] = value.to_dict()

        json_dict = {}
        json_dict['col_order'] = self._col_order
        json_dict['doc_title'] = self._doc_title
        json_dict['setting_map'] = setting_map
        json_dict['default_map'] = default_map

        with open(self._PATH, "w") as json_file:
            json.dump(json_dict, json_file, indent=4)

    @property
    def doc_title(self) -> str:
        """A getter for the document title

        Returns:
             doc_title (str): The document title
	    """
        return self._doc_title

    @doc_title.setter
    def doc_title(self, text: str) -> None:
        """A setter for the doc_title

        Args:
            text (str): the new title
        Rsources:
            - Setter notation:
                https://realpython.com/python-property/#providing-write-only-attributes
        """
        self._doc_title = text
        self.__save_settings()

    @property
    def col_order(self) -> list[int]:
        """A getter for the col_order

        Returns:
             col_order (list[int]): The ordering of the columns
	    """
        return self._col_order

    def reset_col_order(self) -> None:
        """Reset the column ordering (just increasing)"""
        num_cols = len(self.col_order)
        self._col_order = list(range(num_cols))
        self.__save_settings()

    def swap_cols(self, col_one: int, col_two: int) -> None:
        """Swap the column ordering of the two columns

        Args:
            col_one (int): First column to swap
            col_two (int): Second column to swap
        """
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

def main() -> None:
    """main for testing purposes"""

    from src.Font import Font

    settings = Settings()
    num_cols = 2

    default_setting = ColumnSetting()

    for i in range(num_cols):
        settings.update_setting(column=i, setting=default_setting, create_new=True)

    for i in range(num_cols):
        col_setting = settings.get_setting(i)
        print(f"col_setting {i}: {col_setting.to_string()}")

    settings.update_setting(
        column=0,
        setting=ColumnSetting(
            font=Font(font_name="This is garbage"),
            additional_text="lorem ipsum",
        )
    )
    print(f"col_setting 0: {settings.get_setting(0).to_string()}")
    settings.set_to_default(0)
    print(f"col_setting 0: {settings.get_setting(0).to_string()}")

    print(f"col_order: {settings.col_order}")
    settings.swap_cols(
        col_one=0,
        col_two=1,
    )
    print(f"col_order: {settings.col_order}")
    settings.reset_col_order()
    print(f"col_order: {settings.col_order}")

if __name__ == '__main__':
    """main for testing purposes

    Resources:
        - Main:
            https://docs.python.org/3/library/__main__.html
    """
    main()
