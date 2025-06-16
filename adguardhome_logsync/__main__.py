import asyncio

from .main import main as _main


def main():
    """
    Main entry point for the script.
    This function is called when the script is executed directly.
    """
    asyncio.run(_main())


if __name__ == "__main__":
    main()
