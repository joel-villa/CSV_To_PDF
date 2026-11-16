"""The settings for a singular column from the csv"""
from src.Font import Font


class ColumnSetting:
    """The settings of a column"""

    _font: Font
    _is_indicator: bool
    _additional_text: str | None

    def __init__(
        self,
        font: Font,
        is_indicator: bool,
        additional_text: str | None,
    ) -> None:
        """Construct her, I hardly..

        Args:
            font (Font): The font of this column
            is_indicator (bool):  True -> row is a boolean value
            additional_text (str): Any additional text?
	    """
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
