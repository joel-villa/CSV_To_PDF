"""Converts csv's to pdf's"""

import csv
from datetime import datetime
from pathlib import Path

from markdown_pdf import MarkdownPdf, Section

from src.SectionFactory import SectionFactory
from src.Setting import Setting


class Converter:
    """For conversion needs"""

    _settings: Setting
    _section_factory: SectionFactory

    def __init__(
        self,
    ) -> None:
        """Initialize a converter (convert her?)"""
        self._settings = Setting()
        self._section_factory = SectionFactory(self._settings)

    def convert(
        self,
        csv_path: Path,
        pdf_path: Path | None = None,
    ) -> None:
        """Convert the csv to a pdf file

        Args:
            csv (Path): path to the csv file of significance
            pdf (Path | None): path to pdf file

        Resources:
            - Markdown to pdf:
                https://pypi.org/project/markdown-pdf/
            - Current date:
                https://stackoverflow.com/questions/28189442/datetime-current-year-and-month-in-python
            - Reading a csv:
                https://docs.python.org/3/library/csv.html
        """
        if pdf_path is None:
            raise NotImplementedError

        md_pdf = MarkdownPdf()

        # Initial section
        fst_section = f"# {self._settings.doc_title}\n"
        if self._settings.track_date:
            fst_section = f"Last updated {datetime.now().month} {datetime.now().year}\n"
        if self._settings.preamble != "":
            fst_section = f"{fst_section}{self._settings.preamble}\n"
        md_pdf.add_section(Section(fst_section))

        # Reading the csv, using the SectionFactory to create the strings to write
        with open(csv_path) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",", quotechar="|")
            for row in spamreader:
                next_section = Section(self._section_factory.to_section(row))
                md_pdf.add_section(next_section)

        md_pdf.meta["title"] = self._settings.doc_title
        md_pdf.save(pdf_path)


def main() -> None:
    """main for testing purposes"""

    converter = Converter()
    pdf = Path("~/Projects/Personal/CSV_To_PDF/test_out.pdf")
    pdf.touch()
    converter.convert(
        csv_path=Path("~/Projects/Personal/CSV_To_PDF/resources.csv"),
        pdf_path=pdf,
    )


if __name__ == "__main__":
    """main for testing purposes

    Resources:
        - Main:
            https://docs.python.org/3/library/__main__.html
    """
    main()
