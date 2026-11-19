"""The font + color of some text :D"""

from typing import Any


class Font:
    _font_name: str
    _size: int
    _rgb: tuple[int, int, int]
    _is_bold: bool
    _is_italic: bool

    def __init__(
        self,
        font_name: str = "Times-Roman",
        size: int = 24,
        rgb: tuple[int, int, int] = (0, 0, 0),
        is_bold: bool = False,
        is_italic: bool = False,
    ) -> None:
        """Create the Font

        Args:
            font (str): The name of the font
            size (int): Font size
            rbg (tuple [int, int, int]): rgb values
            is_bold (bool): is the font bold?
            is_italic (bool): italics?
        """
        self._font_name = font_name
        self._size = size
        self._rgb = rgb
        self._is_bold = is_bold
        self._is_italic = is_italic

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

    @property
    def is_bold(self) -> bool:
        """A getter for if this font is bold

        Returns:
             is_bold (bool): Is the font bold?
        """
        return self._is_bold

    @property
    def is_italic(self) -> bool:
        """A getter for if this font is bold

        Returns:
             is_italic (bool): Is the font italic?
        """
        return self._is_italic

    def to_dict(self) -> dict[str, Any]:
        """Get the dictionary representation of this Font

        Returns:
             font_dict (dict[str, Any]): Dictionary representation of this Font
        """
        return {
            "font_name": self.font_name,
            "size": self.size,
            "rgb": self.rgb,
            "is_bold": self.is_bold,
            "is_italic": self.is_italic,
        }

    def to_string(self) -> str:
        """String representation of this Font

        Args:
            name (type): Description

        Returns:
             font_str (str): String representation fo this font
        """
        return str(self.to_dict())


def main() -> None:
    """main for testing purposes"""

    font = Font(
        font_name="Times New Roman",
        size=24,
        rgb=(0, 0, 0),
    )

    print(font.font_name)
    print(font.size)
    print(font.rgb)


if __name__ == "__main__":
    """main for testing purposes

    Resources:
        - Main:
            https://docs.python.org/3/library/__main__.html
    """
    main()
