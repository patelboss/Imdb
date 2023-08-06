import logging

logging.basicConfig(filename='bot.log', ...)
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Create a logger instance for the bot
logger = logging.getLogger(__name__)
