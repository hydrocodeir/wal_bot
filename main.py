import uuid
import requests
import json
import datetime
import secrets
import string
import os
import time
import segno
import random
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
    reply_keyboard.add('👤 افزودن کاربر 👤', '🪪 نمایش کاربران 🪪', '💎 مشخصات من 💎','⌛ تمدید کاربر ⌛','🎯 راهنما 🎯', '❌ خارج شدن ❌')
    return reply_keyboard



# start message
@bot.message_handler(commands = ['start'])

def start_message (message):
    chat_id = message.chat.id
    if chat_id == Admin_chat_id:
        bot.send_message(message.chat.id, f'*{STRART_FOR_MAIN_ADMIN}*',parse_mode='markdown', reply_markup = main_admin_menu())
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
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton('❌ بازگشت ❌'))
        msg = bot.send_message(message.chat.id, f'*📘متن قبلی:\n{HELP_MESSAGE}*\n\n ♻️لطفا متن جدید خود را وارد کنید:',parse_mode='markdown', reply_markup=markup)
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

    if message.text == '⌛ تمدید کاربر ⌛':
        if not check_if_logged_in(chat_id):
            bot.send_message(chat_id, "❌ شما وارد نشده‌اید. لطفاً وارد شوید.", reply_markup=markup)
            return
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(KeyboardButton('❌ بازگشت ❌'))
            msg = bot.send_message(message.chat.id, f'*{RENEW_USER}*', parse_mode="markdown",  reply_markup=markup)
            bot.register_next_step_handler(msg, renew_user_step1)

    if message.text == '🎯 راهنما 🎯':
        bot.reply_to(message, f'*{HELP_MESSAGE}*',parse_mode='markdown', reply_markup=admins_menu())

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

    response = "🧑🏻‍💻* لیست ادمین‌ها:*\n\n"
    for admin in admins:
        response += (
            f"```\n👤 یوزرنیم: {admin['user_name']}```\n"
            f"📊 ترافیک باقی‌مانده: {admin['traffic']} GB\n"
            f"🔢 اینباند درحال استفاده: {admin['inb_id']}\n"
            f"\n"
        )


    bot.reply_to(message, response, parse_mode='markdown', reply_markup=markup)

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
            bot.send_message(message.chat.id, f"*✅ ادمین با یوزرنیم: {user_name}، حذف شد *",parse_mode='markdown', reply_markup=main_admin_menu())
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
                bot.send_message(message.chat.id, f'*{START_FOR_ADMINS}*',parse_mode='markdown', reply_markup=admins_menu())
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
            random_numb = random.randint(10, 99)
            user_email[chat_id] = f'{email}{random_numb}'
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
            if admin_traffic < 100:
                warning_text = "⚠️ *هشدار مهم*\n\n" \
                    "🚨 *ترافیک باقی‌مانده شما کمتر از 100 گیگ است!*\n" \
                    "❗ لطفاً بررسی کنید."

                bot.send_message(chat_id, warning_text, parse_mode="Markdown")
                
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
        sub_url = f'https://{sub}/{sub_id}'
        qr = sub_url
        img = segno.make(qr)
        img.save('last_qrcode.png', scale=10, dark='darkblue', data_dark='steelblue')
        img_path = 'last_qrcode.png'
        caption_text = (
            f"🪪*نام کاربری:*  {user_email[chat_id]}\n"
            f"⌛*تعداد روز:*  {user_days[chat_id]}\n"
            f"🔋*سقف ترافیک:*  {gb} GB\n\n"
            f"🔗*لینک سابسکریپشن:*\n"
            f"```\n{sub_url}\n```")
        
        with open(img_path, 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=caption_text, parse_mode="MarkdownV2", reply_markup=admins_menu())

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
    markup.add(KeyboardButton('❌ بازگشت ❌'))
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

        number_to_emoji = {
            0: '0️⃣', 1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣',
            5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣'
        }
        def number_to_emoji_string(number):
            return ''.join(number_to_emoji[int(digit)] for digit in str(number))

        user_list = "📋* لیست کاربران:*\n\n"
        for index, client in enumerate(clients, start=1):
            email = client.get("email", "Unknown")
            expiry_time = client.get("expiryTime", 0)
            remaining_days = 0

            if expiry_time > 0:
                current_time = int(time.time() * 1000)
                remaining_time_ms = expiry_time - current_time
                if remaining_time_ms > 0:
                    remaining_days = int(remaining_time_ms / (1000 * 60 * 60 * 24))
            
            user_list += "```"
            index_emoji = number_to_emoji_string(index)
            user_list += f"\n{index_emoji}| 👤 {email}   (⌛ = {remaining_days}) \n\n"
            user_list += "```"
            if len(user_list) > 3500:
                bot.send_message(chat_id, user_list, parse_mode="Markdown", reply_markup=cancel_button())
                user_list = ""

        user_list += "\n📩 شماره کاربر مورد نظر رو جهت دریافت اطلاعات وارد کنید:"
        bot.send_message(chat_id, user_list, parse_mode="Markdown", reply_markup=cancel_button())

        email_data[chat_id] = clients

        bot.register_next_step_handler_by_chat_id(chat_id, send_sub_id)
    else:
        bot.send_message(chat_id, f"Failed to fetch user list. Status code: {get.status_code}")


def send_sub_id(message):
    chat_id = message.chat.id

    if message.text == "❌ بازگشت ❌":
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

    url = f"https://{panel}/panel/api/inbounds/getClientTraffics/{email}"
    get = s.get(url=url, headers=headers)

    if get.status_code == 200:
        response = get.json()
        sub_url = f'https://{sub}/{sub_id}'
        qr = sub_url
        img = segno.make(qr)
        img.save('last_qrcode.png', scale=10, dark='darkblue', data_dark='steelblue')
        img_path = 'last_qrcode.png'

        obj = response.get('obj', {})
        user_id = obj.get('id')
        #status = obj.get('enable')
        uploaded = obj.get('up')
        downloaded = obj.get('down')
        expiry_time = obj.get('expiryTime')
        total_bytes = obj.get('total')

        usage_traffic = (uploaded + downloaded) / (1024 ** 3)
        total_traffic = total_bytes / (1024 ** 3)

        #expiry_time
        expiry_time_s = expiry_time / 1000
        expiry_date = datetime.datetime.fromtimestamp(expiry_time_s)
        current_time = datetime.datetime.now()
        remaining_time = expiry_date - current_time
        remaining_days = remaining_time.days


        caption_text = (
        f"🪪 *نام کاربری:*  {email}\n"
        f"⌛ *روزهای باقی مانده:*  {remaining_days}\n"
        f"🔋 *ترافیک مصرف شده:*  {usage_traffic:.2f} GB\n"
        f"📦 *کل ترافیک:*  {total_traffic:.2f} GB\n\n"
        f"🔗 *لینک سابسکریپشن:*\n"
        f"```\n{sub_url}\n```"
    )

        with open(img_path, 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=caption_text, parse_mode="Markdown", reply_markup=admins_menu())


# renew user
def renew_user_step1(message):
    if message.text.strip() in ['❌ بازگشت ❌']:
        bot.send_message(message.chat.id, "✅ عملیات لغو شد!", reply_markup=admins_menu())
        return 
    
    email = message.text
    chat_id = message.chat.id

    url = f"https://{panel}/panel/api/inbounds/getClientTraffics/{email}"
    get = s.get(url=url, headers=headers)

    if get.status_code == 200:
        try:
            response = get.json()
        except Exception as e:
            bot.send_message(chat_id, "❌ خطا در پردازش پاسخ از سرور!", parse_mode="markdown", reply_markup=admins_menu())
            return

        obj = response.get('obj')
        if obj is None:
            bot.send_message(chat_id, "❌ کاربر یافت نشد یا اطلاعات نامعتبر است!", parse_mode="markdown", reply_markup=admins_menu())
            return

        gb = obj.get('total', 0) / (1024 ** 3)
        admin_traffic = get_admin_traffic(chat_id)

        if gb > admin_traffic:
            bot.send_message(chat_id, f"❌ ترافیک کافی برای ایجاد کاربر ندارید. (ترافیک شما: {admin_traffic} GB)", reply_markup=admins_menu())
            return
        
        if admin_traffic < 100:
            warning_text = "⚠️ *هشدار مهم*\n\n" \
                "🚨 *ترافیک باقی‌مانده شما کمتر از 100 گیگ است!*\n" \
                "❗ لطفاً بررسی کنید."
            bot.send_message(chat_id, warning_text, parse_mode="Markdown")
                
        if update_admin_traffic(chat_id, -gb):
            inb_id = get_inb_id(chat_id)
            url = f"https://{panel}/panel/api/inbounds/{inb_id}/resetClientTraffic/{email}"
            response = s.post(url=url, headers=headers)

            if response.status_code == 200:
                bot.send_message(chat_id, "*✅ ترافیک کاربر ریست شد، حالا تعداد روز تمدید رو واردکنید:*", parse_mode="markdown")
                bot.register_next_step_handler(message, lambda msg: renew_user_step2(msg, email))
    else:
        bot.send_message(chat_id, "*❌ درخواست با خطا مواجه شد، لطفاً بعداً تلاش کنید!*", parse_mode="markdown", reply_markup=admins_menu())


# renew user step2
def renew_user_step2(message, email):
    if message.text.strip() in ['❌ بازگشت ❌']:
        bot.send_message(message.chat.id, "✅ عملیات لغو شد!", reply_markup=admins_menu())
        return 

    try:
        days = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "❌ لطفاً یک عدد معتبر وارد کنید.", reply_markup=admins_menu())
        return

    chat_id = message.chat.id
    expiry_time = int((datetime.datetime.now() + datetime.timedelta(days=days)).timestamp() * 1000)
    url = f"https://{panel}/panel/api/inbounds/getClientTraffics/{email}"
    get = s.get(url=url, headers=headers)

    if get.status_code == 200:
        inb_id = get_inb_id(chat_id)
        url = f"https://{panel}/panel/api/inbounds/get/{inb_id}"
        response = s.get(url=url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            settings = json.loads(data["obj"]["settings"])
            clients = settings["clients"]

            for client in clients:
                if client['email'] == email:
                    id = client['id']
                    total_gb = client['totalGB']
                    sub_id = client['subId']
                    break

            settings = {
                "clients": [{
                    "id": id,
                    "enable": True,
                    "flow": "",
                    "email": email,
                    "imitIp": "",
                    "totalGB": total_gb,
                    "expiryTime": expiry_time,
                    "tgId": "",
                    "subId": sub_id,
                    "reset": ""
                }]
            }

            proces = {
                "id": inb_id,
                "settings": json.dumps(settings)
            }

            url = f"https://{panel}/panel/api/inbounds/updateClient/{id}"
            res = s.post(url=url, headers=headers, data=proces)

            if res.status_code == 200:
                bot.send_message(chat_id, f'*✅ اشتراک کاربر: {email}، با موفقیت تمدید شد*', parse_mode='markdown', reply_markup=admins_menu())
            else:
                bot.send_message(chat_id, f'*❌ خطا در تمدید: {res.status_code}*', parse_mode='markdown', reply_markup=admins_menu())
        else:
            bot.send_message(chat_id, f'*❌ خطا در دریافت اطلاعات کلاینت: {response.status_code}*', parse_mode='markdown', reply_markup=admins_menu())
    else:
        bot.send_message(chat_id, f'*❌ خطا در دریافت `inb_id`: {get.status_code}*', parse_mode='markdown', reply_markup=admins_menu())






# save new help message
def save_new_help_message (message):
    if message.text == '❌ بازگشت ❌':
        return bot.send_message(message.chat.id, "✅ عملیات ویرایش راهنما لغو شد.", reply_markup= main_admin_menu())
    
    new_text = message.text.strip()
    change_help_message("message.py", "HELP_MESSAGE", new_text)

    bot.send_message(message.chat.id, '✅متن راهنما با موفقیت تغییر یافت.', reply_markup= main_admin_menu())
    os.system("systemctl restart wal_bot.service")







if __name__ == "__main__":
    bot.polling()