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

    def write_line(self, font: Font, text: str) -> None:
        """Write the line into the pdf in the given font

        Args:
            font (Font): The font of the text to write
            text (str): The text to put in the pdf

	    """
        raise NotImplementedError
