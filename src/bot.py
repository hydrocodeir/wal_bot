from telebot import TeleBot
from config import bot
from handlers import handlers, message_handlers
from log.logger_config import logger
import time







if __name__ == "__main__":
    logger.info("Wall bot started")
    try:
        bot.polling(non_stop=True)

    except Exception as e:
        logger.error(f"Wall bot crashed: {e}")
        time.sleep(2)
    

