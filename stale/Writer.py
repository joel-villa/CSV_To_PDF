"""For writing lines to a PDF (all ReportLab stuff goes here)"""

from reportlab.pdfgen import canvas
from reportlab.pdfgen.textobject import PDFTextObject

from stale.Font import Font


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

    _pdf: canvas.Canvas
    _text: PDFTextObject | None

    def __init__(self, pdf_path: str) -> None:
        """Create the PDF Writer

        Args:
            pdf_path (str): Path to the pdf file to create

        Resrouces:
            - String splitting:
                https://www.geeksforgeeks.org/python/python-string-till-substring/
        """
        self._pdf = canvas.Canvas(pdf_path)

        # Ensure document title is not a path (no '/''s and no extension')
        document_title = pdf_path.split("/")[-1]
        doc_title_list = document_title.split(".")[:-1]
        document_title = "".join(doc_title_list)
        print(f"document_title: {document_title}")  # TODO: delete this
        self._pdf.setTitle(document_title)
        self._text = None

    def write_line(self, text: str, font: Font, is_title: bool = False) -> None:
        """Write the line into the pdf in the given font

        Args:
            text (str): The text to put in the pdf
            font (Font): The font of the text to write
        """
        if is_title:
            self._pdf.setFillColorRGB(*font.rgb)
            self._pdf.setFont(
                psfontname=font.font_name,
                size=font.size,
            )
            self._pdf.drawCentredString(x=300, y=770, text=text)
        else:
            if self._text is None:
                # Initializing the text box :D
                self._text = self._pdf.beginText(40, 680)

            self._text.setFillColorRGB(*font.rgb)
            self._text.setFont(
                psfontname=font.font_name,
                size=font.size,
            )
            self._text.textLine(text=text)

    def finish(self) -> None:
        if self._text is not None:
            self._pdf.drawText(self._text)

        self._pdf.save()


def main() -> None:
    """main for testing purposes"""

    writer = Writer("test.pdf")

    fonts = ["Times-Roman", "Courier", "Helvetica"]
    sizes = [24, 32, 64]
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

    writer.finish()


if __name__ == "__main__":
    """main for testing purposes

    Resources:
        - Main:
            https://docs.python.org/3/library/__main__.html
    """
    main()
