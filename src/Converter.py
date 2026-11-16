"""For converting csv's to pdf's"""
from pathlib import Path

from src.Settings import Settings


class Converter:

    _settings: Settings

    def __init__(
        self,
        settings: Settings,
    ) -> None:
        """Initialize a converter (convert her?)

        Args:
            settings (Settings): The settings of this converter
        """
        self._settings = settings

    def convert(
        self,
        csv: Path,
        pdf: Path | None = None,
    ) -> None:
        """Convert the csv to a pdf file

        Args:
            csv (Path): path to the csv file of significance
            pdf (Path | None): path to pdf file (if None, just do in directory
            with the same name as the csv--do replacing handling)
    	"""
        raise NotImplementedError
