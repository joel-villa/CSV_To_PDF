"""The Interface for interacting with the user"""

# NOTE: should be useable without CLI: just put .pdf in same location as csv (do not override anything existing)

from pathlib import Path

from src.Setting import Setting


class CLI:
    """The Command Line Interface"""

    _settings: Setting

    def __init__(
        self,
        settings: Setting,
    ) -> None:
        """Construct that CLI ASAP

        Args:
            settings (Settings): converter settings
        """
        if settings.read_only:
            raise ValueError("Setting needs to be writable for the CLI")
        self._settings = settings

    def run(self) -> Path:
        """Do all that user interaction goodness

        Args:
            name (type): Description

        Returns:
             csv_path (Path): The path to the csv file
        """
        raise NotImplementedError


def main() -> None:
    """main for testing purposes"""

    settings = Setting()
    cli = CLI(settings)
    path = cli.run
    print(path)


if __name__ == "__main__":
    """main for testing purposes

    Resources:
        - Main:
            https://docs.python.org/3/library/__main__.html
    """
    main()
