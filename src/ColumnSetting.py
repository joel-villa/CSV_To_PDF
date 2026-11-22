"""The setting for a singular CSV column"""

from typing import Any


class ColumnSetting:
    """The settings of a column"""

    _read_only: bool
    _is_bold: bool
    _is_italic: bool
    _contains_hyperlink: bool
    _header_number: int
    _indicator_text: str | None
    # TODO: markdown header?

    def __init__(
        self,
        is_bold: bool = False,
        is_italic: bool = False,
        contains_hyperlink: bool = False,
        header_number: int = 0,
        indicator_text: str | None = None,
        read_only: bool = True,
    ) -> None:
        """The setting of a specific column

        Args:
            is_bold (bool): Should this column be bold?
            is_italic (bool): Should this coolumn be italicized
            contains_hyperlink (bool): Does this column contain a hyper link?
            header_number (int): The header number of this column
            indicator_text (str | None): Is this column an indicator one? If
            so it has some default text
            read_only (bool): Is this Column Setting not to be updated?
        """
        self._read_only = read_only
        self._is_bold = is_bold
        self._is_italic = is_italic
        self._contains_hyperlink = contains_hyperlink
        self._header_number = header_number
        self._indicator_text = indicator_text

    def __check_authorization(self) -> None:
        """Check that this column setting is allowed to be written to"""
        if self._read_only:
            raise ValueError("This Column Setting is read only")

    def __str__(self) -> str:
        """Get the string reperesentation of this column settiing

        Args:
            name (type): Description

        Returns:
            col_setting_string (str): String reperesentation

        Resources:
            toString in Python:
                https://stackoverflow.com/questions/16768302/does-python-have-a-tostring-equivalent-and-can-i-convert-a-class-to-string
        """
        return str(self.to_dict())

    @property
    def is_bold(self) -> bool:
        """A getter for is_bold

        Returns:
            is_bold (bool): Should this column be bold?
        """
        return self._is_bold

    @property
    def is_italic(self) -> bool:
        """A getter for is_italic

        Returns:
            is_italic (bool): Should this coolumn be italicized
        """
        return self._is_italic

    @property
    def contains_hyperlink(self) -> bool:
        """A getter for contains_hyperlink

        Returns:
            contains_hyperlink (bool): Does this column contain a hyper link?
        """
        return self._contains_hyperlink

    @property
    def header_number(self) -> int:
        """A getter for header_number

        Returns:
            header_number (int): The header number of this column
        """
        return self._header_number

    @property
    def indicator_text(self) -> str | None:
        """A getter for indicator_text

        Returns:
            indicator_text (str | None): Is this column an indicator one? If
            so it has some default text
        """
        return self._indicator_text

    @is_bold.setter
    def is_bold(self, new_val: bool) -> None:
        """A setter for is_bold

        Args:
            new_val (bool): The new value for the property
        """
        self.__check_authorization()
        self._is_bold = new_val

    @is_italic.setter
    def is_italic(self, new_val: bool) -> None:
        """A setter for is_italic

        Args:
            new_val (bool): The new value for the property
        """
        self.__check_authorization()
        self._is_italic = new_val

    @contains_hyperlink.setter
    def contains_hyperlink(self, new_val: bool) -> None:
        """A setter for contains_hyperlink

        Args:
            new_val (bool): The new value for the property
        """
        self.__check_authorization()
        self._contains_hyperlink = new_val

    @header_number.setter
    def header_number(self, new_val: int) -> None:
        """A setter for header_number

        Args:
            new_val (bool): The new value for the property
        """
        self.__check_authorization()
        self._header_number = new_val

    @indicator_text.setter
    def indicator_text(self, new_val: str | None) -> None:
        """A setter for indicator_text

        Args:
            new_val (str): The new value for the property
        """
        self.__check_authorization()
        self._indicator_text = new_val

    def to_dict(self) -> dict[str, Any]:
        """a dictionary representation of this column

        Args:
            name (type): Description

        Returns:
             col_setting_dict (dict): Dictionary representation of this setting
        """
        return {
            "is_bold": self._is_bold,
            "is_italic": self._is_italic,
            "contains_hyperlink": self._contains_hyperlink,
            "header_number": self._header_number,
            "indicator_text": self._indicator_text,
        }


def main() -> None:
    """main for testing purposes"""
    col_setting = ColumnSetting(read_only=False)
    print(f"col_setting: {col_setting}")

    col_setting.indicator_text = "is an indicator"
    col_setting.is_bold = True
    col_setting.is_italic = True

    print(f"col_setting: {col_setting}")

    immutable_col_setting = ColumnSetting(read_only=True, **col_setting.to_dict())

    print(f"immutable_col_setting: {col_setting}")

    try:
        immutable_col_setting.indicator_text = None
    except ValueError as e:
        print(e)

    try:
        immutable_col_setting.is_bold = False
    except ValueError as e:
        print(e)

    try:
        immutable_col_setting.is_italic = False
    except ValueError as e:
        print(e)

    try:
        immutable_col_setting.contains_hyperlink = True
    except ValueError as e:
        print(e)

    print(f"immutable_col_setting: {col_setting}")


if __name__ == "__main__":
    """main for testing purposes"""
    main()
