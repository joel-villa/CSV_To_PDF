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
