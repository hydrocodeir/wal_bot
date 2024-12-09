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
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
from api import *

load_dotenv()


bot = TeleBot(os.getenv("BOT_TOKEN"))
Admin_chat_id = int(os.getenv("ADMIN_CHAT_ID"))
# Admin menu
def admin_menu ():
    markup = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton('👤 Add admin', callback_data= 'add_sellers')
    button2 = InlineKeyboardButton('👁️ Show admins', callback_data= 'show_sellers')
    button3 = InlineKeyboardButton('❌ Delete admin', callback_data= 'del_sellers')
    markup.add(button1, button2, button3)
    return markup



# Sellers menu
def seller_menu ():
    markup = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton('👤 Add User', callback_data= 'add_user_')
    button2 = InlineKeyboardButton('🪪 Show Users', callback_data= 'Show_users_')
    markup.add(button1, button2)
    return markup

# return button for admin
def return_button_admin ():
    markup = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton('♻️ Return ♻️', callback_data= 'cancel')
    markup.add(button)
    return markup


# start message
@bot.message_handler(commands = ['start'])

def start_message (message):
    chat_id = message.chat.id
    if chat_id == Admin_chat_id:
        bot.send_message(message.chat.id, STRART_FOR_ADMIN, reply_markup = admin_menu())
    elif is_seller(chat_id):
        bot.send_message(message.chat.id, START_FOR_SELLERS, reply_markup = seller_menu())
    else:
        bot.send_message(message.chat.id, 'this bot not is for you !!!')


# callback
@bot.callback_query_handler(func=lambda call: True)
def callback_handler (call):

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == 'cancel':
        bot.edit_message_text(STRART_FOR_ADMIN, chat_id=chat_id, message_id=message_id, reply_markup=admin_menu())

    if call.data == 'cancel2':
        bot.edit_message_text(STRART_FOR_ADMIN, chat_id=chat_id, message_id=message_id, reply_markup=seller_menu())

    if call.data == 'add_sellers':
        bot.edit_message_text('enter chat id', chat_id=chat_id, message_id=message_id, reply_markup=return_button_admin())
        bot.register_next_step_handler(call.message, add_seller_step1)

    if call.data == 'show_sellers':
        message = "Sellers List:\n" + "\n".join([str(seller) for seller in get_all_sellers()])
        bot.edit_message_text(message, chat_id=chat_id, message_id=message_id, reply_markup=return_button_admin())
    
    if call.data == 'del_sellers':
        bot.edit_message_text('enter admin id for delete', chat_id=chat_id, message_id=message_id, reply_markup=return_button_admin())
        bot.register_next_step_handler(call.message, Del_seller)

    if call.data == 'add_user_':
        bot.edit_message_text(ADD_EMAIL, chat_id=chat_id, message_id=message_id)
        bot.register_next_step_handler(call.message, add_user_step1)

    if call.data == 'Show_users_':
        send_emails_with_buttons(call.message.chat.id)




# add sellers func
def add_seller_step1(message):
    if message.content_type == 'text':
        try:
            seller_id = int(message.text)
            bot.send_message(message.chat.id, 'Enter inbound id for this seller:')
            bot.register_next_step_handler(message, lambda msg: add_seller_step2(msg, seller_id))
        except ValueError:
            bot.send_message(message.chat.id, 'Please send a valid seller ID.')

def add_seller_step2(message, seller_id):
    if message.content_type == 'text':
        try:
            inb_id = int(message.text)
            if add_seller(seller_id, inb_id):
                bot.send_message(message.chat.id, f'Seller added: ID={seller_id}, Inbound id={inb_id}', reply_markup=admin_menu())
            else:
                bot.send_message(message.chat.id, 'Seller already exists.')
        except ValueError:
            bot.send_message(message.chat.id, 'Please send a valid number.')


#del seller
def Del_seller(message):
    if message.content_type == 'text': 
        try:
            delete_id = int(message.text)
            delete_seller(delete_id)
            bot.send_message(message.chat.id, f"Seller with ID {delete_id} has been deleted.", reply_markup=admin_menu())
        except ValueError:
            bot.send_message(message.chat.id, "Please enter a valid numeric ID.")
        except Exception as e:
            bot.send_message(message.chat.id, f"An error occurred: {e}")



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
            bot.send_message(chat_id, 'Please send the number of days:')
            bot.register_next_step_handler(message, add_user_step2)
        except Exception as e:
            bot.send_message(message.chat.id, f"Error: {e}")


def add_user_step2(message):
    if message.content_type == 'text':
        chat_id = message.chat.id
        try:
            days = int(message.text)
            user_days[chat_id] = days
            bot.send_message(chat_id, "Please enter the volume in GB:")
            bot.register_next_step_handler(message, add_user_step3)
        except ValueError:
            bot.send_message(chat_id, "Invalid input. Please enter a valid number for days.")
            bot.register_next_step_handler(message, add_user_step2)


def add_user_step3(message):
    if message.content_type == 'text':
        chat_id = message.chat.id
        try:
            gb = int(message.text)
            user_gb[chat_id] = gb

            bot.send_message(chat_id, f"User details:\nEmail: {user_email[chat_id]}\nDays: {user_days[chat_id]}\nVolume: {user_gb[chat_id]} GB")
            
            add_user_f(chat_id)
        except ValueError:
            bot.send_message(chat_id, "Invalid input. Please enter a valid number for GB.")
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

        bot.send_message(chat_id, f"✅ User added successfully \n\n👇 Subscription for [ {email} ]\n\nhttps://{sub}/{sub_id}")
        bot.send_message(chat_id, START_FOR_SELLERS, reply_markup=seller_menu())

        clear_user_data(chat_id)
    else:
        bot.send_message(chat_id, f"Failed to add user. Error: {res2.text}")


def clear_user_data(chat_id):
    user_email.pop(chat_id, None)
    user_days.pop(chat_id, None)
    user_gb.pop(chat_id, None)




def send_emails_with_buttons(chat_id):
    url = f"https://{panel}/panel/api/inbounds/get/2"

    get = s.get(url=url, headers=headers)

    if get.status_code == 200:
        data = get.json()
        settings = json.loads(data["obj"]["settings"])
        clients = settings["clients"]

        emails = [client["email"] for client in clients if "email" in client]

        if not emails:
            bot.send_message(chat_id, "No emails found.")
            return

        markup = InlineKeyboardMarkup(row_width=1)
        for email in emails:
            url = f"https://{panel}/panel/api/inbounds/getClientTraffics/{email}"
            res = s.get(url=url)
            res_data = res.json()
    

            status = '✅' if res_data.get("obj", {}).get("enable", False) else '❌'

            expiry_time = res_data.get("obj", {}).get("expiryTime", 0)
            remaining_days = 0  
            if expiry_time > 0:
                current_time = int(time.time() * 1000)
                remaining_time_ms = expiry_time - current_time

                if remaining_time_ms > 0:
                    remaining_days = int(remaining_time_ms / (1000 * 60 * 60 * 24))


            button = InlineKeyboardButton(
                text=f'name: {email} | status: {status} |  time remaining: {remaining_days} D',
                callback_data=email
            )
            markup.add(button)


        return_button = InlineKeyboardButton(text="♻️ Return ♻️", callback_data="cancel2")
        markup.add(return_button)

        bot.send_message(chat_id, "This section is being updated...", reply_markup=markup)
    else:
        bot.send_message(chat_id, f"Failed to fetch emails. Status code: {get.status_code}")












bot.polling()