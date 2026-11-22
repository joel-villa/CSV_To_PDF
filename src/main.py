"""You know the vibes, a runnable main, the actual entry point for the
program"""

from src.CLI import CLI
from src.Converter import Converter


def main() -> None:
    """Runnnable main

    Resources:
        - Path to string:
            https://stackoverflow.com/questions/21518476/python-path-as-a-string
    """

    cli = CLI()
    csv_path, pdf_path = cli.run()
    converter = Converter()
    converter.convert(
        csv_path=csv_path,
        pdf_path=pdf_path,
    )

    print(f"A pdf file was successfully created at \"{pdf_path}\"")

if __name__ == "__main__":
    """Runnnable main"""
    main()
