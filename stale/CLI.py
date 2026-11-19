"""The Command Line Interface"""
from pathlib import Path

from stale.Settings import Settings


class CLI:
    """The Command Line Interface"""

    _settings: Settings

    def __init__(
        self,
        settings: Settings,
    ) -> None:
        """Construct that CLI ASAP

        Args:
            settings (Settings): converter settings
        """
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

    settings = Settings()
    cli = CLI(settings)
    path = cli.run
    print(path)


if __name__ == '__main__':
    """main for testing purposes

    Resources:
        - Main:
            https://docs.python.org/3/library/__main__.html
    """
    main()
