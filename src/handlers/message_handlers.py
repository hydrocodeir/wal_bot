from handlers.handlers import admins_page, save_new_help_message, add_user_step1, send_emails_, renew_user_step1, admins_menu, delete_user_step1, get_admin_info
from db.query import admins_query
from messages.messages import *
from config import bot
from telebot.types import InlineKeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from api import *




# message handler
@bot.message_handler(func=lambda call: True)
def message_handler (message):
    chat_id = message.chat.id
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="👤 Login 👤", callback_data="login")
    markup.add(button1)

    if message.text == '👤 نمایندگان':
        return admins_page(message)
    
    if message.text == '📘 متن راهنما':
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton('❌ بازگشت ❌'))
        msg = bot.send_message(chat_id, f'*📘متن قبلی:\n{HELP_MESSAGE}*\n\n ♻️لطفا متن جدید خود را وارد کنید:',parse_mode='markdown', reply_markup=markup)
        bot.register_next_step_handler(msg, save_new_help_message)

    if message.text == '👤 افزودن کاربر 👤':
        if not admins_query.admin_approval(chat_id):
            bot.send_message(chat_id, "❌ شما وارد نشده‌اید. لطفاً وارد شوید.", reply_markup=markup)
            return
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(KeyboardButton('❌ بازگشت ❌'))
            bot.send_message(chat_id, ADD_EMAIL , reply_markup=markup)
            bot.register_next_step_handler(message, lambda msg: add_user_step1(msg))

    if message.text == '🪪 نمایش کاربران 🪪':
        if not admins_query.admin_approval(chat_id):
            bot.send_message(chat_id, "❌ شما وارد نشده‌اید. لطفاً وارد شوید.", reply_markup=markup)
            return
        else:
            send_emails_(chat_id)

    if message.text == '⌛ تمدید کاربر ⌛':
        if not admins_query.admin_approval(chat_id):
            bot.send_message(chat_id, "❌ شما وارد نشده‌اید. لطفاً وارد شوید.", reply_markup=markup)
            return
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(KeyboardButton('❌ بازگشت ❌'))
            msg = bot.send_message(chat_id, f'*{RENEW_USER}*', parse_mode="markdown",  reply_markup=markup)
            bot.register_next_step_handler(msg, renew_user_step1)

    if message.text == '🎯 راهنما 🎯':
        bot.reply_to(message, f'*{HELP_MESSAGE}*',parse_mode='markdown', reply_markup=admins_menu())

    if message.text == '🗑️ حذف کاربر 🗑️':
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton('❌ بازگشت ❌'))
        msg = bot.send_message(chat_id, '⚠️نام کاربر مورد نظر رو جهت حذف کاربر ارسال کنید:', reply_markup=markup)
        bot.register_next_step_handler(msg, delete_user_step1)

    if message.text == '❌ خارج شدن ❌':
        if admins_query.remove_chat_id(chat_id):
            bot.send_message(chat_id, '❌ شما از پنل مدیریتی خود خارج شدید ، جهت استفاده مجدد لاگین کنید:', reply_markup=markup)
            return
        else:
            pass
        
    if message.text == "💎 مشخصات من 💎":
        if not admins_query.admin_approval(chat_id):
            bot.send_message(chat_id, "❌ شما وارد نشده‌اید. لطفاً وارد شوید.", reply_markup=markup)
            return
        else:
            get_admin_info(chat_id)
