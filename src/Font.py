"""The font + color of some text :D"""

class Font:
    _font_name: str
    _size: int
    _rgb: tuple[int, int, int]


    def __init__(
        self,
        font_name: str,
        size: int,
        rgb: tuple[int, int, int]
    ) -> None:
        """Create the Font

        Args:
            font (str): The name of the font
            size (int): Font size
            rbg (tuple [int, int, int]): rgb values
	    """
        self._font_name = font_name
        self._size = size
        self._rgb = rgb

    @property
    def font_name(self) -> str:
        """A getter for the font

        Returns:
             font (str): The name of the font
	    """
        return self._font_name

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

    def to_dict(self) -> dict[str, Any]:
        """Get the dictionary representation of this Font

        Returns:
             font_dict (dict[str, Any]): Dictionary representation of this Font
	    """
        return {
            'font_name': self.font_name,
            'size': self.size,
            'rgb': self.rgb,
        }


def main() -> None:
    """main for testing purposes"""

    font = Font(
        font_name='Times New Roman',
        size=24,
        rgb=(0, 0, 0),
    )

    print(font.font_name)
    print(font.size)
    print(font.rgb)

if __name__ == '__main__':
    """main for testing purposes

    Resources:
        - Main:
            https://docs.python.org/3/library/__main__.html
    """
    main()
