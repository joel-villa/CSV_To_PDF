"""Settings, ooh, how profesional"""

from pathlib import Path

from src.ColumnSetting import ColumnSetting


class Settings:
    """The settings object"""

    _setting_map: dict[int, ColumnSetting]
    _col_order: list[int]
    _PATH_DEFAULT: Path
    _PATH: Path

    def __init__(self) -> None:
        """Loads the setting map from the settings path
	    """
        raise NotImplementedError

    def __load_settings(self) -> None:
        """Load the settings from the settings path"""
        raise NotImplementedError

    def __save_settings(self) -> None:
        """Save the settings to the settings path"""
        raise NotImplementedError

    @property
    def col_order(self) -> list[int]:
        """A getter for the col_order

        Returns:
             col_order (list[int]): The ordering of the columns
	    """
        return self._col_order

    def update_setting(self, column: int, setting: ColumnSetting) -> None:
        """Update the setting for the specific column

        Args:
            column (int): The column number
            setting (ColumnSetting): The column setting
	    """
        self._setting_map[column] = setting

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
