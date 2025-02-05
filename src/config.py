from telebot import TeleBot
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__),'db', '.env')
load_dotenv(dotenv_path=dotenv_path)


BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
PANEL_ADDRES = os.getenv("PANEL_ADDRESS")
SUB_ADDRES = os.getenv("SUB_ADDRESS")

bot = TeleBot(BOT_TOKEN)
Admin_chat_id = ADMIN_CHAT_ID