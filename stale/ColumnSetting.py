"""The settings for a singular column from the csv"""

from typing import Any

from stale.Font import Font


class ColumnSetting:
    """The settings of a column"""

    _font: Font
    _is_indicator: bool
    _additional_text: str | None

    def __init__(
        self,
        font: Font | None = None,
        is_indicator: bool = False,
        additional_text: str | None = None,
    ) -> None:
        """Construct her, I hardly..

        Args:
            font (Font): The font of this column
            is_indicator (bool):  True -> row is a boolean value
            additional_text (str): Any additional text?
        """
        if font is None:
            font = Font()
        self._font = font
        self._is_indicator = is_indicator
        self._additional_text = additional_text

    @property
    def font(self) -> Font:
        """A getter for the font

        Returns:
             font (Font): The font of this column
        """
        return self._font

    @property
    def is_indicator(self) -> bool:
        """A getter for is_indicator

        Returns:
             is_indicator (bool):  True -> row is a boolean value
        """
        return self._is_indicator

    @property
    def additional_text(self) -> str | None:
        """A getter for additional_text

        Returns:
             additional_text (str): Any additional text?
        """
        return self._additional_text

    def to_dict(self) -> dict[str, Any]:
        """Get the dictionary representation of a ColumnSetting

        Returns:
             setting_dict (dict[str, Any]): The dictionary representation of
             this object
        """
        return {
            "font": self.font.to_dict(),
            "is_indicator": self.is_indicator,
            "additional_text": self.additional_text,
        }

    def to_string(self) -> str:
        """Get the string representation of this setting

        Returns:
            string (str): string represenatation
        Resources:
            - dict to str:
                https://www.geeksforgeeks.org/python/python-convert-dictionary-object-into-string/
        """
        dict = self.to_dict()
        return str(dict)


def main() -> None:
    """main for testing purposes"""

    default_setting = ColumnSetting(
        font=Font(
            font_name="Times New Roman",
            size=24,
            rgb=(0, 0, 0),
        ),
        is_indicator=False,
        additional_text=None,
    )

    print(default_setting.font.font_name)
    print(default_setting.font.size)
    print(default_setting.font.rgb)
    print(default_setting.additional_text)
    print(default_setting.is_indicator)


if __name__ == "__main__":
    """main for testing purposes

    Resources:
        - Main:
            https://docs.python.org/3/library/__main__.html
    """
    main()
