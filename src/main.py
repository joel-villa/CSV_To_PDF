"""You know the vibes, a runnable main, the actual entry point for the
program"""

from src.CLI import CLI
from src.Converter import Converter


def main() -> None:
    """main for testing purposes"""

    cli = CLI()
    csv_path, pdf_path = cli.run()
    converter = Converter()
    converter.convert(
        csv_path=csv_path,
        pdf_path=pdf_path,
    )


if __name__ == "__main__":
    """main for testing purposes

    Resources:
        - Main:
            https://docs.python.org/3/library/__main__.html
    """
    main()
