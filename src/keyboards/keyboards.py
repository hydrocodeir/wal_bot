from telebot.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)



# main admin menu
def main_admin_menu():
    reply_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False, row_width=2
    )
    reply_keyboard.add("👤 نمایندگان", "⚙️ تنظیمات")
    return reply_keyboard


# setting menu
def setting_menu():
    reply_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False, row_width=2
    )
    reply_keyboard.add(
        "💵 پلن پیش پرداخت",
        "💸 پلن پس پرداخت",
        "💻 پنل ها",
        "📘 متن راهنما",
        "🧾 متن ثبت نام",
        "🔔 نوتیف ها",
        "🗂 پشتیبان گیری",
        "🔙 بازگشت",
    )
    return reply_keyboard

# backup menu
def backup_menu():
    reply_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False, row_width=2
    )

    reply_keyboard.add(
        "📥 دریافت بکاپ",
        "📤 بازگردانی بکاپ",
        "🔙 بازگشت",
    )
    return reply_keyboard

# change notif status
def notif_status_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(
        text="🔄️ استارت", callback_data="change_start_notif_status"
    )
    button2 = InlineKeyboardButton(
        text="🔄️ ایجاد کاربر", callback_data="change_create_notif_status"
    )
    button3 = InlineKeyboardButton(
    text="🔄️ حذف کاربر", callback_data="change_delete_notif_status"
    )
    markup.add(button1, button2, button3)
    return markup


# admins menu
def admins_menu():
    reply_keyboard = ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True, one_time_keyboard=False
    )
    reply_keyboard.add(
        "👤 افزودن کاربر",
        "🪪 نمایش کاربران",
        "💎 مشخصات من",
        "🎯 راهنما",
        "🛒 شارژ حساب",
        "❌ خارج شدن",
    )
    return reply_keyboard

def buy_traffic():
    reply_keyboard = ReplyKeyboardMarkup(
        row_width=1, resize_keyboard=True, one_time_keyboard=False
    )
    reply_keyboard.add("💵 خرید ترافیک","♻️ بازگشت")
    return reply_keyboard

def debt_and_buy_traffic():
    reply_keyboard = ReplyKeyboardMarkup(
        row_width=1, resize_keyboard=True, one_time_keyboard=False
    )
    reply_keyboard.add(
        "💵 خرید ترافیک",
        "💳 پس پرداخت",
        "♻️ بازگشت"
    )
    return reply_keyboard

# admins page
def admins_control():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(
        text="⚙️ مدیریت نماینده", callback_data="modify_admin"
    )
    button2 = InlineKeyboardButton(
        text="➕ افزودن نماینده", callback_data="add_an_admin"
    )
    markup.add(button1, button2)
    return markup

def admin_modify_control(user_name):
    markup = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(
        text="🔋 افزودن ترافیک", callback_data=f"add_traffic_{user_name}"
    )
    button2 = InlineKeyboardButton(
        text="🪫 کاهش ترافیک", callback_data=f"reduse_traffic_{user_name}"
    )
    button3 = InlineKeyboardButton(
        text="🆔 تغییر ایدی پنل", callback_data=f"change_panel_{user_name}"
    )
    button4 = InlineKeyboardButton(
        text="🆔 تغییر ایدی اینباند", callback_data=f"change_inb_{user_name}"
    )
    button5 = InlineKeyboardButton(
        text="♻️ فعال/غیرفعال", callback_data=f"status_for_{user_name}"
    )
    button6 = InlineKeyboardButton(
        text="❌ حذف نماینده", callback_data=f"delete_admin_{user_name}"
    )
    markup.add(button1, button2, button3, button4, button5, button6)
    return markup


# plans page
def plans_control():
    markup = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(
        text="📋 افزودن پلن", callback_data="add_a_plan"
    )
    button2 = InlineKeyboardButton(
        text="⚙️ ویرایش پلن", callback_data="change_plan"
    )
    button3 = InlineKeyboardButton(
        text="❌ حذف پلن", callback_data="delete_plan"
    )
    button4 = InlineKeyboardButton(
        text="💳 تنظیم شماره کارت", callback_data="set_card"
    )
    markup.add(button1, button2, button3, button4)
    return markup

def debt_control():
    markup = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(
        text="🔄️ فعال/غیرفعال", callback_data="change_debt_status"
    )
    button2 = InlineKeyboardButton(
        text="💸 ثبت قیمت", callback_data="change_debt_price"
    )
    button3 = InlineKeyboardButton(
        text="📅 ثبت مهلت پرداخت", callback_data="dead_line"
    )
    markup.add(button1, button2, button3)
    return markup


def payment_methods():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(
        text="💳 کارت به کارت", callback_data="card_payment"
    )
    markup.add(button1)
    return markup

def payment_methods_for_debt():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(
        text="💳 کارت به کارت", callback_data="card_payment_for_debt"
    )
    markup.add(button1)
    return markup

def panels_control():
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(
        text="➕ افزودن پنل", callback_data="add_panel"
    )
    button2 = InlineKeyboardButton(
        text="⚙️ تغییر اطلاعات پنل", callback_data="edit_panel"
    )
    button3 = InlineKeyboardButton(
        text="❌ حذف پنل", callback_data="delete_panel"
    )
    markup.add(button1, button2, button3)
    return markup

def user_control(email):
    markup = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(
        text="❌ حذف کاربر", callback_data=f"delete_user_{email}"
    )
    button2 = InlineKeyboardButton(
        text="🔄️ تمدید کاربر", callback_data=f"renew_user_{email}"
    )
    markup.add(button1, button2)
    return markup