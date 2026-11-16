"""For writing lines to a PDF (all ReportLab stuff goes here)"""

from pathlib import Path

from src.Font import Font


class Writer:
    """Writes to a PDF file

    Resources:
        - ReportLab Tutorial:
            https://www.geeksforgeeks.org/python/creating-pdf-documents-with-python/
        - Adding a Link to a PDF:
            https://stackoverflow.com/questions/78433781/how-to-add-a-link-to-an-object-in-a-pdf-using-reportlab
        - Python classing:
            https://docs.python.org/3/tutorial/classes.html
    """
    def __init__(self, pdf_path: Path) -> None:
        """Create the PDF Writer

        Args:
            pdf_path (Path): Path to the pdf file to create
	    """
        raise NotImplementedError

    def write_line(self, text: str, font: Font) -> None:
        """Write the line into the pdf in the given font

        Args:
            text (str): The text to put in the pdf
            font (Font): The font of the text to write
	    """
        raise NotImplementedError


def main() -> None:
    """main for testing purposes"""

    writer = Writer(Path("test"))

    fonts = [
        'Times New Roman',
        'Courier',
        'Calibri'
    ]
    sizes = [
        24,
        32,
        64
    ]
    rgbs = [
        (0, 0, 0),
        (255, 0, 0),
        (0, 255, 0),
    ]
    text = "Lorem ipsum type shit"

    for i, font_name in enumerate(fonts):
        font = Font(
            font_name=font_name,
            size=sizes[i],
            rgb=rgbs[i],
        )
        writer.write_line(
            text=text,
            font=font,
        )


if __name__ == '__main__':
    """main for testing purposes

    Resources:
        - Main:
            https://docs.python.org/3/library/__main__.html
    """
    main()
