"""Settings, ooh, how profesional"""

import json
from pathlib import Path

from src.ColumnSetting import ColumnSetting
from src.Font import Font


class Settings:
    """The settings object"""

    _setting_map: dict[int, ColumnSetting]
    _default_map: dict[int, ColumnSetting]
    _doc_title: str
    _col_order: list[int]
    _PATH: Path = Path("settings/settings.json")
    _PATH_DEFAULT: Path = Path("settings/default_settings.json")

    def __init__(self) -> None:
        """Loads the setting map from the settings path
	    """
        self._setting_map = {}
        self._default_map = {}
        self._col_order = [0]
        #TODO title + subtitle saving
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

            setting_map = setting_dict['setting_map']
            #TODO: finish settings reading + writing implementation
            #TODO: col_order

            for key, value in setting_map.items():
                font = Font(**value['font'])
                self._setting_map[int(key)] = ColumnSetting(
                    font=font,
                    is_indicator=value['is_indicator'],
                    additional_text=value['additional_text'],
                )

        with open(self._PATH_DEFAULT) as f:
            setting_map = json.load(f)

            for key, value in setting_map.items():
                print(f"value: {value}")
                font = Font(**value['font'])
                self._setting_map[int(key)] = ColumnSetting(
                    font=font,
                    is_indicator=value['is_indicator'],
                    additional_text=value['additional_text'],
                )

    def __save_settings(self) -> None:
        """Save the settings to the settings path"""
        print(f"in save_settings: {self._setting_map}")
        with open(self._PATH, "w") as f:
            json.dump(self._setting_map, f, indent=4)

    @property
    def col_order(self) -> list[int]:
        """A getter for the col_order

        Returns:
             col_order (list[int]): The ordering of the columns
	    """
        return self._col_order

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

    def update_setting(self, column: int, setting: ColumnSetting) -> None:
        """Update the setting for the specific column

        Args:
            column (int): The column number
            setting (ColumnSetting): The column setting
	    """
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
    print(settings.col_order)
    num_cols = len(settings.col_order)

    default_setting = ColumnSetting(
        font=Font(
            font_name='Times New Roman',
            size=24,
            rgb=(0, 0, 0),
        ),
        is_indicator=False,
        additional_text=None,
    )

    for i in range(num_cols):
        settings.update_setting(column=i, setting=default_setting)

    for i in range(num_cols):
        col_setting = settings.get_setting(i)
        print(col_setting.font.font_name)
        print(col_setting.font.size)
        print(col_setting.font.rgb)
        print(col_setting.additional_text)
        print(col_setting.is_indicator)

if __name__ == '__main__':
    """main for testing purposes

    Resources:
        - Main:
            https://docs.python.org/3/library/__main__.html
    """
    main()
