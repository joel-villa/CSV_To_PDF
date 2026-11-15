"""The font + color of some text :D"""

class Font:
    _font: str
    _size: int
    _rgb: tuple[int, int, int]


    def __init__(
        self,
        font: str,
        size: int,
        rgb: tuple[int, int, int]
    ) -> None:
        """Create the Font

        Args:
            font (str): The name of the font
            size (int): Font size
            rbg (tuple [int, int, int]): rgb values
	    """
        self._font = font
        self._size = size
        self._rgb = rgb

    @property
    def font(self) -> str:
        """A getter for the font

        Returns:
             font (str): The name of the font
	    """
        return self._font

    @property
    def size(self) -> int:
        """A getter for the font size

        Returns:
             size (int): The font size
	    """
        return self._size

    @property
    def rgb(self) -> tuple[int, int, int]:
        """A getter for the rgb color

        Returns:
             rgb (tuple[int, int, int]): The rgb color
	    """
        return self._rgb
