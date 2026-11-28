"""Makes Sections based on some Settings"""

import numpy as np

from src.Setting import Setting


class SectionFactory:
    """Creates Sections (string representation of rows) based on settings"""

    _setting: Setting

    def __init__(
        self,
        setting: Setting,
    ) -> None:
        """Create a Section Factory

        Args:
            setting (Setting): Configuration of file output
        """
        self._setting = setting

    def to_section(self, field_values: list[str]) -> str:
        """Create a section given the field values

        Args:
            field_values (list[str]): The values for each field (column) of a
            singular row of the csv

        Returns:
             section (str): The markdownified string representation of the row

        Resources:
            - Indices that would sort an array:
                https://numpy.org/doc/stable/reference/generated/numpy.argsort.html
            - Markdown syntax:
                https://www.markdownguide.org/basic-syntax/
            - Duplicating a string's text:
                https://www.geeksforgeeks.org/python/create-multiple-copies-of-a-string-in-python-by-using-multiplication-operator/
        """

        section = ""

        for i in self._setting.col_order:
            field_value = field_values[i]
            field_setting = self._setting.get_setting(i)
            is_header = self._setting.col_order[i] == 0
            field_str = ""

            if field_value == "":
                continue

            if field_value[0] == '"' and field_value[-1] == '"':
                field_value = field_value[1:-1]
                # Cleaning data

            if field_setting.contains_hyperlink:
                # Field value is a hyper link! make it so
                field_value = f"[{field_value}]({field_value})"

            if is_header:
                # Header value is a special case: no field_name, and need ##
                field_str = f"{field_value}"
            else:
                field_str = f"{field_setting.name}: {field_value}"

            if field_setting.indicator_text is not None:
                if field_setting.contains_hyperlink:
                    field_str = f"{field_value}"
                else:
                    if field_setting.contains_hyperlink:
                        field_str = f"[{field_setting.indicator_text}]({field_setting.indicator_text})"
                    field_str = f"{field_setting.indicator_text}"

            if field_setting.is_bold and not field_setting.is_italic:
                field_str = f"**{field_str}**"

            if field_setting.is_italic and not field_setting.is_bold:
                field_str = f"*{field_str}*"

            if field_setting.is_italic and field_setting.is_bold:
                field_str = f"***{field_str}***"

            header_str = "#" * field_setting.header_number

            field_str = f"{header_str} {field_str}"

            section = f"{section}{field_str}  \n"

        return section


def main() -> None:
    """main for testing purposes"""
    section_factory = SectionFactory()
    section_factory.field_names = ["name", "age", "favorite color"]
    print(section_factory.to_section(["Bob", "29", "purple"]))
    print(section_factory.to_section(["Alice", "31", "cyan"]))
    print(section_factory.to_section(["Sick Fuck", "30", "green"]))


if __name__ == "__main__":
    """main for testing purposes"""
    main()
