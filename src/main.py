import argparse
import logging
from logging_config import setup_logging
from app import create_app
import os
import config

logger = logging.getLogger("main")

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    setup_logging(
        log_file="logs/main.log", 
        console_level=logging.DEBUG if args.debug else logging.INFO
    )
   
    #logger.debug(config.AppConfig.SYNLOGY_CHAT_WEBHOOK_URL)

    app = create_app()

    app.run(
        host="0.0.0.0",
        port=config.AppConfig.PORT
    )

if __name__ == "__main__":
    main()