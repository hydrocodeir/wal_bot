from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from db.query import price_query




# main admin menu
def main_admin_menu ():
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False,row_width=2)
    reply_keyboard.add('👤 نمایندگان', '⚙️ پلن ها', '📘 متن راهنما', '🧾 متن ثبت نام')
    return reply_keyboard



# admins menu
def admins_menu ():
    reply_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    reply_keyboard.add('👤 افزودن کاربر 👤',
                        '🪪 نمایش کاربران 🪪',
                        '💎 مشخصات من 💎',
                        '⌛ تمدید کاربر ⌛',
                        '🎯 راهنما 🎯',
                        '🗑️ حذف کاربر 🗑️',
                        '💵 خرید ترافیک 💵',
                        '❌ خارج شدن ❌')
    return reply_keyboard

# admins page
def admins_controll():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text='👤 افزودن ادمین 👤', callback_data='add_an_admin')
    button2 = InlineKeyboardButton(text='♻️ تغییر اینباند ادمین ♻️', callback_data='change_inb')
    button3 = InlineKeyboardButton(text='🔋 افزودن ترافیک به ادمین 🔋', callback_data='add_traffic')
    button4 = InlineKeyboardButton(text= '❌ حذف ادمین ❌', callback_data='delete_admin')
    markup.add(button1, button2, button3, button4)
    return markup

# plans page
def plans_controll():
    markup = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text='📋 افزودن پلن 📋', callback_data='add_a_plan')
    button2 = InlineKeyboardButton(text='⚙️ ویرایش پلن ⚙️', callback_data='change_plan')
    button3 = InlineKeyboardButton(text= '❌ حذف پلن ❌', callback_data='delete_plan')
    button4 = InlineKeyboardButton(text= '💳 تنظیم شماره کارت 💳', callback_data='set_card')
    markup.add(button1, button2, button3, button4)
    return markup

def payment_methods():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text='💳 کارت به کارت 💳', callback_data='card_payment')
    markup.add(button1)
    return markup


