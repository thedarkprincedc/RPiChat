import argparse
from app import create_app
from .config import AppConfig

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    app = create_app(args.debug)

    app.run(
        host="0.0.0.0",
        port=AppConfig.RPI_PORT
    )

if __name__ == "__main__":
    main()