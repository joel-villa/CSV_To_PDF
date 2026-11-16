"""The Command Line Interface"""
from pathlib import Path

from src.Settings import Settings


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
