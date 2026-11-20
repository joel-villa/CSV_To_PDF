"""Makes Sections based on some Settings"""

from src.Setting import Setting


class SectionFactory:
    """Creates Sections (string representation of rows) based on settings"""

    _setting: Setting
    _field_names: list[str] | None

    def __init__(
        self,
        setting: Setting | None = None,
    ) -> None:
        """Create a Section Factory

        Args:
            setting (Setting): Configuration of file output
        """
        self._field_names = None

        if setting is None:
            self._setting = Setting()
        else:
            self._setting = setting

    @property
    def field_names(self):
        """Need a getter, even though I don't need a getter (so I can use a
        setter)

        Returns:
             NOTHING, raises an error, field_names is write only!
        """
        raise AttributeError("field_names is write_only")

    @field_names.setter
    def field_names(self, value: list[str]) -> None:
        """A setter for field_names

        Args:
            value (list[str]): The field names of the columns

        Resources:
            - Write only class variables:
                https://realpython.com/python-property/#providing-write-only-attributes
        """
        if self._field_names is not None:
            # TODO: do we really need to do this? May be too handholdy (be cautious of throwing ERRORS is good coding practices)
            raise AttributeError(
                f"field_names is not allowed to be overrideable, currently has value of: {self._field_names}"
            )
        self._field_names = value

    def to_section(self, field_values: list[str]) -> str:
        """Create a section given the field values

        Args:
            field_values (list[str]): The values for each field (column) of a
            singular row of the csv

        Returns:
             section (str): The markdownified string representation of the row
        """
        if self._field_names is None:
            # TODO: handle Null field_names
            raise NotImplementedError
        raise NotImplementedError

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
