"""Converts csv's to pdf's"""

import csv
from datetime import datetime
from pathlib import Path

from markdown_pdf import MarkdownPdf, Section

from src.SectionFactory import SectionFactory
from src.Setting import Setting


class Converter:
    """For conversion needs"""

    def convert(
        self,
        csv_path: Path,
        pdf_path: Path | None = None,
        setting_title: str | None = None,
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
            - Reading a file:
                https://www.geeksforgeeks.org/python/read-file-as-string-in-python/
        """
        if pdf_path is None:
            raise NotImplementedError
        setting: Setting
        section_factory: SectionFactory
        section = ""

        md_pdf = MarkdownPdf()


        # Reading the csv, using the SectionFactory to create the strings to write
        with open(csv_path) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",", quotechar='"')
            column_names = next(spamreader)

            if setting_title is None:
                # Default settings when setting_title is None
                setting = Setting(field_names=column_names)
            else:
                setting = Setting(title=setting_title)

            # Initial section
            section = f"# {setting.title}\n"
            if setting.track_date:
                section = f"{section}Last updated {datetime.now().strftime('%B')} {datetime.now().year}  \n"
            if setting.preamble != "":
                section = f"{section}{setting.preamble}  \n"

            # The section factory!
            section_factory = SectionFactory(setting)

            for row in spamreader:
                section = f"{section}{section_factory.to_section(row)}"

        file_path = "style.css"
        with open(file_path, "r") as file:
            css_settings = file.read()

        md_pdf.add_section(
            Section(section),
            user_css=css_settings,
        )
        md_pdf.meta["title"] = setting.title
        md_pdf.toc = []

        pdf_path.touch()
        md_pdf.save(pdf_path)


def main() -> None:
    """main for testing purposes"""

    converter = Converter()
    pdf = Path("test_out.pdf")
    converter.convert(
        csv_path=Path("resources.csv"),
        pdf_path=pdf,
    )


if __name__ == "__main__":
    """main for testing purposes

    Resources:
        - Main:
            https://docs.python.org/3/library/__main__.html
    """
    main()
