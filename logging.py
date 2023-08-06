import logging

# Set up logging
logging.basicConfig(filename='bot.py',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Create a logger instance for the bot
logger = logging.getLogger(__name__)
