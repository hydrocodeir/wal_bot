import uuid
import requests
import json
import datetime
import secrets
import string
import os
import time
from createdata import *
from message import *
from telebot import TeleBot, types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from api import *

load_dotenv()


bot = TeleBot(os.getenv("BOT_TOKEN"))
Admin_chat_id = int(os.getenv("ADMIN_CHAT_ID"))
# main admin menu
def main_admin_menu ():
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False,row_width=2)
    reply_keyboard.add('👤 ادمین ها', '📘 متن راهنما')
    return reply_keyboard



# admins menu
def admins_menu ():
    reply_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    reply_keyboard.add('👤 افزودن کاربر 👤', '🪪 نمایش کاربران 🪪', '💎 مشخصات من 💎','🎯 راهنما 🎯', '❌ خارج شدن ❌')
    return reply_keyboard

# return button for admin
def return_button_admin ():
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_keyboard.add('♻️ بازگشت ♻️')
    return reply_keyboard


# start message
@bot.message_handler(commands = ['start'])

def start_message (message):
    chat_id = message.chat.id
    if chat_id == Admin_chat_id:
        bot.send_message(message.chat.id, STRART_FOR_MAIN_ADMIN, reply_markup = main_admin_menu())
    else:
        markup = InlineKeyboardMarkup(row_width=1)
        button1 = InlineKeyboardButton(text="👤 Login 👤", callback_data="login")
        markup.add(button1)
        bot.send_message(message.chat.id, '🎯 جهت استفاده از این ربات باید لاگین کنید.', reply_markup=markup)


# message handler
@bot.message_handler(func=lambda call: True)
def message_handler (message):
    chat_id = message.chat.id
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="👤 Login 👤", callback_data="login")
    markup.add(button1)

    if message.text == '👤 ادمین ها':
        return admins_page(message)
    
    if message.text == '📘 متن راهنما':
        if str(message.chat.id) != Admin_chat_id:
            return bot.send_message(message.chat.id, "❌ شما اجازه دسترسی ندارید.")
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton('❌ بازگشت ❌'))
        msg = bot.send_message(message.chat.id, 'متن راهنمای جدید را ارسال کنید:')
        bot.register_next_step_handler(msg, save_new_help_message)

    if message.text == '👤 افزودن کاربر 👤':
        if not check_if_logged_in(chat_id):
            bot.send_message(chat_id, "❌ شما وارد نشده‌اید. لطفاً وارد شوید.", reply_markup=markup)
            return
        else:
            bot.send_message(chat_id, ADD_EMAIL , reply_markup=admins_menu())
            bot.register_next_step_handler(message, lambda msg: add_user_step1(msg))

    if message.text == '🪪 نمایش کاربران 🪪':
        if not check_if_logged_in(chat_id):
            bot.send_message(chat_id, "❌ شما وارد نشده‌اید. لطفاً وارد شوید.", reply_markup=markup)
            return
        else:
            send_emails_(chat_id)

    if message.text == '🎯 راهنما 🎯':
        bot.reply_to(message, HELP_MESSAGE)

    if message.text == '❌ خارج شدن ❌':
        if check_if_logged_in(chat_id):
            logout_user(chat_id)
            bot.send_message(message.chat.id, '❌ شما از پنل مدیریتی خود خارج شدید ، جهت استفاده مجدد لاگین کنید:', reply_markup=markup)
            logout_user(chat_id)
            return
        else:
            pass
        
    if message.text == "💎 مشخصات من 💎":
        if not check_if_logged_in(chat_id):
            bot.send_message(chat_id, "❌ شما وارد نشده‌اید. لطفاً وارد شوید.", reply_markup=markup)
            return
        else:
            get_admin_info(chat_id)

        



# admins page
def admins_page(message):
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text='👤 افزودن ادمین 👤', callback_data='add_an_admin')
    button2 = InlineKeyboardButton(text='♻️ تغییر اینباند ادمین ♻️', callback_data='change_inb')
    button3 = InlineKeyboardButton(text='🔋 افزودن ترافیک به ادمین 🔋', callback_data='add_traffic')
    button4 = InlineKeyboardButton(text= '❌ حذف ادمین ❌', callback_data='del_admin')
    markup.add(button1, button2, button3, button4)

    admins = get_all_admins()
    if not admins:
        bot.reply_to(message, "❌ هیچ ادمینی ثبت نشده است.", reply_markup=markup)
        return

    response = "🧑🏻‍💻 لیست ادمین‌ها:\n\n"
    for admin in admins:
        response += (
            f"👤 یوزرنیم: {admin['user_name']}\n"
            f"📊 ترافیک باقی‌مانده: {admin['traffic']} GB\n"
            f"🔢 اینباند درحال استفاده: {admin['inb_id']}\n"
            f"------------------------\n"
        )

    bot.reply_to(message, response, reply_markup=markup)

#callback handler
@bot.callback_query_handler(func=lambda call: True)
def callback_handler (call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if call.data == 'add_an_admin':
        bot.edit_message_text(text=ADD_ADMIN_1, chat_id=chat_id, message_id=message_id)
        bot.register_next_step_handler(call.message, add_admin_step1)

    if call.data == 'change_inb':
        bot.edit_message_text(text=CHANGE_INB_ID, chat_id=chat_id, message_id=message_id)
        bot.register_next_step_handler(call.message, edit_inb_step1)

    if call.data == 'add_traffic':
        bot.edit_message_text(text='یوزرنیم ادمین مورد نظر رو جهت افزایش ترافیک وارد کنید:', chat_id=chat_id, message_id=message_id)
        bot.register_next_step_handler(call.message, add_traffic_step1)

    if call.data == 'del_admin':
        bot.edit_message_text(text='یوزر نیم ادمین مورد نظر رو جهت حذف کردن واردکنید:', chat_id=chat_id, message_id=message_id)
        bot.register_next_step_handler(call.message, Del_admin)

    if call.data == "login":
        bot.edit_message_text(text='لطفا یوزرنیم خود را وارد کنید:',chat_id=chat_id, message_id=message_id)
        bot.register_next_step_handler(call.message, login_step1)

    if call.data == 'cancel':
        bot.edit_message_text(text=START_FOR_ADMINS, chat_id=chat_id, message_id=message_id, reply_markup=admins_menu)
        



# add admin func
def add_admin_step1(message):
    if message.content_type == 'text':
        try:
            user_name = message.text
            bot.send_message(message.chat.id, ADD_ADMIN_2)
            bot.register_next_step_handler(message, lambda msg: add_admin_step2(msg, user_name))
        except ValueError:
            bot.send_message(message.chat.id, '❌ Please send a valid world.')

def add_admin_step2(message, user_name):
    if message.content_type == 'text':
        try:
            password = message.text
            bot.send_message(message.chat.id, ADD_ADMIN_3)
            bot.register_next_step_handler(message, lambda msg: add_admin_step3(msg, user_name, password))
        except ValueError:
            bot.send_message(message.chat.id, '❌ Please send a valid world.')

def add_admin_step3(message, user_name, password):
    if message.content_type == 'text':
        try:
            traffic = int(message.text)
            bot.send_message(message.chat.id, ADD_ADMIN_4)
            bot.register_next_step_handler(message, lambda msg: add_admin_step4(msg, user_name, password, traffic))
        except ValueError:
            bot.send_message(message.chat.id, '❌ Please send a valid world.')
            

def add_admin_step4 (message, user_name, password, trafiic):
    if message.content_type == 'text':
        try:
            inb_id = int(message.text)
            if add_admin(user_name, password, trafiic, inb_id):
                bot.send_message(message.chat.id, f'✅ ادمین اضافه شد: \n\n👤username: {user_name} \n\n🔐password: {password} \n\n🔋total trafiic: {trafiic}', reply_markup=main_admin_menu())
            else:
                bot.send_message(message.chat.id, 'admin already exists.')
        except ValueError:
            bot.send_message(message.chat.id, '❌ Please send a valid number.')
#add traffic
def add_traffic_step1(message):
    if message.content_type == 'text':
        try:
            user_name = message.text
            bot.send_message(message.chat.id, 'حالا ترافیک مد نظر رو به گیگابایت وارد کنید:')
            bot.register_next_step_handler(message, lambda msg: add_traffic_step2(msg, user_name))
        except ValueError:
            bot.send_message(message.chat.id, "Please enter a valid world.")


def add_traffic_step2(message, user_name):
    if message.content_type == 'text':
        try:
            traffic = int(message.text)
            if add_traffic_for_admin(user_name, traffic):
                bot.send_message(message.chat.id, '✅ ترافیک با موفقیت اضافه شد')
            else:
                bot.send_message(message.chat.id, '❌ کاربری با این نام پیدا نشد ')
        except ValueError:
            bot.send_message(message.chat.id, '❌ Please send a valid number.')


#edit inb id
def edit_inb_step1(message):
    if message.content_type == 'text':
        try:
            user_name = message.text
            bot.send_message(message.chat.id, 'حالا اینباند ادمین مورد نظر را وارد کنید:')
            bot.register_next_step_handler(message, lambda msg: edit_inb_step2(msg, user_name))
        except ValueError:
            bot.send_message(message.chat.id, "Please enter a valid world.")

def edit_inb_step2(message, user_name):
    if message.content_type == 'text':
        try:
            new_inb = int(message.text)
            bot.send_message(message.chat.id, '✅ اینباد ادمین موردنظر تغییر یافت')
            change_inb_id(user_name, new_inb)

        except ValueError:
            bot.send_message(message.chat.id, "Please enter a valid numeric ID.")


#del admins
def Del_admin(message):
    if message.content_type == 'text': 
        try:
            user_name = message.text
            delete_admin(user_name)
            bot.send_message(message.chat.id, f"ادمین با یوزرنیم: {user_name} \n✅ حذف شد ", reply_markup=main_admin_menu())
        except Exception as e:
            bot.send_message(message.chat.id, f"An error occurred: {e}")


#login
def login_step1(message):
    if message.content_type == 'text': 
        try:
            user_name = message.text
            bot.send_message(message.chat.id, 'حالا پسورد خود را وارد کنید:')
            bot.register_next_step_handler(message, lambda msg: login_step2(msg, user_name))
        except ValueError:
            bot.send_message(message.chat.id, "Please enter a valid world.")

def login_step2(message, user_name):
    if message.content_type == 'text':
        try:
            password = message.text
            chat_id = message.chat.id
            if login_user(user_name, password, chat_id) and save_admin_login(chat_id, user_name):
                bot.send_message(message.chat.id, '👑 خوش آمدید! وارد سیستم شدید.')
                bot.send_message(message.chat.id, START_FOR_ADMINS, reply_markup=admins_menu())
            else:
                bot.send_message(message.chat.id, '❌  /start .پسورد یا نام کاربری اشتباه است.')
        except ValueError:
            bot.send_message(message.chat.id, "Please enter a valid world.")

#check logged
def check_if_logged_in(chat_id):
    return chat_id in logged_in_users




# add user
user_email = {}
user_days = {}
user_gb = {}

def add_user_step1(message):
    if message.content_type == 'text':
        try:
            chat_id = message.chat.id
            email = str(message.text).strip()
            user_email[chat_id] = email
            bot.send_message(chat_id, ADD_DAYS)
            bot.register_next_step_handler(message, add_user_step2)
        except Exception as e:
            bot.send_message(message.chat.id, f"Error: {e}")


def add_user_step2(message):
    if message.content_type == 'text':
        chat_id = message.chat.id
        try:
            days = int(message.text)
            user_days[chat_id] = days
            bot.send_message(chat_id, ADD_TRAFFIC)
            bot.register_next_step_handler(message, add_user_step3)
        except ValueError:
            bot.send_message(chat_id, "Invalid input. Please enter a valid number for days.")
            bot.register_next_step_handler(message, add_user_step2)


def add_user_step3(message):
    if message.content_type == 'text':
        chat_id = message.chat.id
        try:
            gb = int(message.text)
            if gb <= 0:
                bot.send_message(chat_id, "❌ لطفاً مقدار ترافیک معتبر و مثبت وارد کنید.")
                bot.register_next_step_handler(message, add_user_step3)
                return

            admin_traffic = get_admin_traffic(chat_id)

            if admin_traffic is None:
                bot.send_message(chat_id, "❌ مشکلی در اطلاعات شما وجود دارد.")
                return
            
            if gb > admin_traffic:
                bot.send_message(chat_id, f"❌ ترافیک کافی برای ایجاد کاربر ندارید. (ترافیک شما: {admin_traffic} GB)")
                return

            if update_admin_traffic(chat_id, -gb):
                user_gb[chat_id] = gb
                add_user_f(chat_id)
            else:
                bot.send_message(chat_id, "❌ مشکلی در به‌روزرسانی ترافیک پیش آمد.")
        except ValueError:
            bot.send_message(chat_id, "❌ مقدار وارد شده صحیح نیست. لطفاً یک عدد معتبر وارد کنید.")
            bot.register_next_step_handler(message, add_user_step3)






def generate_secure_random_text(length=16):
    characters = string.ascii_letters + string.digits
    secure_text = ''.join(secrets.choice(characters) for _ in range(length))
    return secure_text

def add_user_f(chat_id):
    email = user_email.get(chat_id)
    days = user_days.get(chat_id)
    gb = user_gb.get(chat_id)
    
    bytes_value = int(gb * 1024 * 1024 * 1024)
    expiry_time = int((datetime.datetime.now() + datetime.timedelta(days=days)).timestamp() * 1000)
    sub_id = generate_secure_random_text(16)

    add = f"https://{panel}/panel/inbound/addClient"
    c_uuid = str(uuid.uuid4())



    settings = {"clients": [{
    "id": c_uuid,
    "enable": True,
    'flow': "",
    "email": email,
    "imitIp":"",
    "totalGB": bytes_value,
    "expiryTime": expiry_time,
    "tgId": "",
    "subId": sub_id,
    "reset": ""
    }]}

    inb_id = get_inb_id(chat_id)
    proces = {
        "id": inb_id,
        "settings": json.dumps(settings)
    }

    res2 = s.post(add, proces)

    if res2.status_code == 200:

        bot.send_message(chat_id, 
                        f"کاربر باموفقیت ساخته شد ✅\n\n"
                        f"👤: {user_email[chat_id]}\n"
                        f"⌛: {user_days[chat_id]}\n"
                        f"🔋: {gb} GB\n-----------\n"
                        f"لینک سابسکریپشن کاربر 👇 \n\nhttps://{sub}/{sub_id}")
        
        bot.send_message(chat_id, START_FOR_ADMINS, reply_markup=admins_menu())

        clear_user_data(chat_id)
    else:
        bot.send_message(chat_id, f"Failed to add user. Error: {res2.text}")


def clear_user_data(chat_id):
    user_email.pop(chat_id, None)
    user_days.pop(chat_id, None)
    user_gb.pop(chat_id, None)

#get info 
def get_admin_info(chat_id):
    admin_traffic = get_admin_traffic(chat_id)
    if admin_traffic is None:
        bot.send_message(chat_id, "❌ مشکلی در دریافت اطلاعات شما وجود دارد.")
        return

    bot.send_message(
        chat_id,
        f"👤 مشخصات شما:\n🔋 ترافیک باقی‌مانده: {admin_traffic} GB",
        reply_markup=admins_menu()
    )
    
# show clients
email_data={}

def cancel_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("❌ کنسل"))
    return markup


def send_emails_(chat_id):
    inb_id = get_inb_id(chat_id)
    url = f"https://{panel}/panel/api/inbounds/get/{inb_id}"

    get = s.get(url=url, headers=headers)

    if get.status_code == 200:
        try:
            data = get.json()
        except requests.exceptions.JSONDecodeError:
            bot.send_message(chat_id, "Error: Response is not a valid JSON")
            return

        settings = json.loads(data["obj"]["settings"])
        clients = settings["clients"]

        if not clients:
            bot.send_message(chat_id, "No users found.")
            return

        user_list = "📋 لیست یوزرها:\n\n"
        for index, client in enumerate(clients, start=1):
            email = client.get("email", "Unknown")
            expiry_time = client.get("expiryTime", 0)
            remaining_days = 0

            if expiry_time > 0:
                current_time = int(time.time() * 1000)
                remaining_time_ms = expiry_time - current_time
                if remaining_time_ms > 0:
                    remaining_days = int(remaining_time_ms / (1000 * 60 * 60 * 24))

            user_list += f"{index}️⃣ 👤 :{email}  |  روزهای باقی مانده: {remaining_days}\n\n"

        user_list += "\n📩 عدد یوزر مورد نظر رو جهت دریافت لینک ساب وارد:"
        bot.send_message(chat_id, user_list, reply_markup=cancel_button())

        email_data[chat_id] = clients

        bot.register_next_step_handler_by_chat_id(chat_id, send_sub_id)
    else:
        bot.send_message(chat_id, f"Failed to fetch user list. Status code: {get.status_code}")


def send_sub_id(message):
    chat_id = message.chat.id

    if message.text == "❌ کنسل":
        bot.send_message(chat_id, "✅ عملیات لغو شد.", reply_markup=admins_menu())
        return

    if not message.text.isdigit():
        bot.send_message(chat_id, "❌ لطفاً فقط عدد وارد کنید.", reply_markup=cancel_button())
        bot.register_next_step_handler(message, send_sub_id)
        return

    user_index = int(message.text) - 1

    if chat_id not in email_data or user_index < 0 or user_index >= len(email_data[chat_id]):
        bot.send_message(chat_id, "❌ شماره وارد شده معتبر نیست. لطفاً دوباره امتحان کنید.", reply_markup=cancel_button())
        bot.register_next_step_handler(message, send_sub_id)
        return

    selected_user = email_data[chat_id][user_index]
    email = selected_user.get("email", "Unknown")
    sub_id = selected_user.get("subId", "Sub ID not found")

    bot.send_message(chat_id, f"👤 نام کاربری: {email}\n\n🔑 لینک سابسکریپشن: https://{sub}/{sub_id}", reply_markup=admins_menu())


# save new help message
def save_new_help_message (message):
    if message.text == '❌ بازگشت ❌':
        return bot.send_message(message.chat.id, "✅ عملیات ویرایش راهنما لغو شد.")
    
    new_text = message.text.strip()
    change_help_message("message.py", "HELP_MESSAGE", new_text)

    bot.send_message(message.chat.id, 'متن راهنما برای ادمین ها با موفقیت تغییر یافت✅')








if __name__ == "__main__":
    bot.polling()