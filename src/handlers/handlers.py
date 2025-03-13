from keyboards.keyboards import (
    main_admin_menu,
    setting_menu,
    backup_menu,
    admins_menu,
    notif_status_menu,
    admins_control,
    payment_methods_for_debt,
    plans_control,
    buy_traffic,
    debt_and_buy_traffic,
    debt_control,
    payment_methods,
    admin_modify_control

)
from pay.card_method import receive_photo_step, receive_photo_step_for_debt
from db.query import (
    admins_query,
    price_query,
    traffic_price_query,
    card_number_query,
    help_message_query,
    registering_message,
    setting_query,
)
from config import bot, Admin_chat_id, PANEL_ADDRES, SUB_ADDRES
from handlers.notifications import notif_setting
import utils
import uuid
import requests
import datetime
import secrets
import string
import os
import time
import segno
import random
import json
from messages.messages import messages_setting
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from api import PanelAPI

api = PanelAPI()
data = {"username": os.getenv("PANEL_USER"), "password": os.getenv("PANEL_PASS")}
sub = SUB_ADDRES


# start message
@bot.message_handler(commands=["start"])
def start_message(message):
    chat_id = message.chat.id
    if chat_id == Admin_chat_id:
        bot.send_message(
            Admin_chat_id,
            f"*{messages_setting.START_ADMIN}*",
            parse_mode="markdown",
            reply_markup=main_admin_menu(),
        )
    else:
        if setting_query.show_start_notif() == True:
            notif_setting.start_notif(message)
        if admins_query.admin_data(chat_id):
            bot.send_message(message.chat.id, messages_setting.START_NONE_SUDO, reply_markup=admins_menu())
        else:
            markup = InlineKeyboardMarkup(row_width=1)
            button1 = InlineKeyboardButton(
                text="👤 Register 👤", callback_data="Register"
            )
            button2 = InlineKeyboardButton(text="👤 Login 👤", callback_data="login")
            markup.add(button1, button2)
            bot.send_message(
                message.chat.id,
                "🎯 جهت استفاده از این ربات باید ریجستر یا لاگین کنید.",
                reply_markup=markup,
            )


# admins page
def admins_page(message):
    admins = admins_query.show_admins()
    if not admins:
        bot.reply_to(
            message, "❌ هیچ ادمینی ثبت نشده است.", reply_markup=admins_control()
        )
        return
    else:
        response = "🧑🏻‍💻<b> لیست نمایندگان:</b>\n\n"
        for admin in admins:
            admin_debt_traffic = admin["debt"]
            price = traffic_price_query.show_price()
            debt = admin_debt_traffic * price  
                
            traffic = admin['traffic']
            if traffic == "false":
                traffic = 0
                
            response += (
                f"<pre>👤 یوزرنیم: {admin['user_name']}</pre>\n"
                f"🔐 پسورد: {admin['password']}\n"
                f"🔢 اینباند درحال استفاده: {admin['inb_id']}\n"
                f"📊 ترافیک باقی‌مانده: {traffic} GB\n"
                f"💸 بدهی: {debt} تومان\n"
                f"\n"
            )
        bot.reply_to(
            message, response, parse_mode="HTML", reply_markup=admins_control()
        )


# settings page/menu
def settings_page(message):
    bot.send_message(
        message.chat.id, "⚙️ وارد منوی تنظیمات شدید", reply_markup=setting_menu()
    )


def return_to_main_menu(message):
    bot.send_message(
        message.chat.id, "🔙 به منوی اصلی برگشتید", reply_markup=main_admin_menu()
    )


# notif page
def get_notif_status_text():
    start_notif = setting_query.show_start_notif()
    create_notif = setting_query.show_create_notif()
    delete_notif = setting_query.show_delete_notif()

    start_notif_status = "✅" if start_notif else "❌"
    create_notif_status = "✅" if create_notif else "❌"
    delete_notif_status = "✅" if delete_notif else "❌"

    response = (
        f"🔔 <b>Notification Status</b>\n"
        f"<b>وضعیت نوتیفیکیشن‌ها:</b>\n\n"
        f"<b>({start_notif_status}) استارت ربات</b> \n"
        f"<b>({create_notif_status}) ساخت کاربر توسط نماینده</b> \n"
        f"<b>({delete_notif_status}) حذف کاربر توسط نمایندگان</b> \n"
    )
    return response


def notif_page(message):

    response = get_notif_status_text()
    bot.send_message(
        message.chat.id,
        response,
        parse_mode="HTML",
        reply_markup=notif_status_menu(),
    )


# plans page
def plans_page(message):
    plans = price_query.show_plans()
    if not plans:
        bot.reply_to(
            message, "❌هیچ پلنی ساخته نشده است", reply_markup=plans_control()
        )
        return
    else:
        response = "📋* لیست پلن های نمایندگی:*\n\n"
        for plan in plans:
            response += (
                f"```\n🔢 ایدی پلن: {plan['id']}```\n"
                f"📊 ترافیک: {plan['traffic']} GB\n"
                f"💵 قیمت : {plan['price']} T\n"
                f"\n"
            )
        bot.reply_to(
            message, response, parse_mode="markdown", reply_markup=plans_control()
        )

def show_plans(message):
    chat_id = message
    get_status = admins_query.admin_data(chat_id)  
    user_status = get_status["traffic"]

    if user_status.lower() == "false":
        user_status = False
    
    if not setting_query.show_debt_stasus() or not user_status:
        if get_status["debt"] > 0:
            bot.send_message(chat_id, "⚠️ قبل از هر خریدی اول حساب خود را در بخش مشخصات من تسویه کنید")
        else:
            bot.send_message(chat_id, "⬇️ روش های فعال جهت شارژ حساب", reply_markup=buy_traffic())
    else:
        bot.send_message(chat_id, "⬇️ روش های فعال جهت شارژ حساب", reply_markup=debt_and_buy_traffic())


def show_plans_with_button(message):
    plans = price_query.show_plans()
    if not plans:
        bot.send_message(message, "هیچ پلنی جهت خرید موجود نیست❕")
        return
    else:
        response = "📋* لیست پلن های موجود (قیمت ها به تومان!)*"
        markup = InlineKeyboardMarkup(row_width=1)

        for plan in plans:
            button_text = f"ترافیک: {plan['traffic']} GB - قیمت: {plan['price']} T"
            button = InlineKeyboardButton(
                text=button_text, callback_data=f"select_plan_{plan['id']}"
            )
            markup.add(button)
        bot.send_message(message, response, reply_markup=markup, parse_mode="Markdown")


# debt page
def debt_status_text():
    status = setting_query.show_debt_stasus()

    debt_status = "✅" if status else "❌"
    response = (
        f"<b>⚠️ پلن پس پرداخت به برمبنای استفاده هر 1 گیگ توسط نماینده هااست.</b>\n\n"
        f"<b>وضعیت پلن پس پرداخت ({debt_status})</b>"
    )
    return response

def debt_page(message):
    response = debt_status_text()
    bot.reply_to(
        message,
        response,
        parse_mode="HTML",
        reply_markup=debt_control()
    )
    
# debt contract
def debt_contract(message):
    chat_id = message.chat.id
    get_username = admins_query.admin_data(chat_id)
    user_name = get_username["user_name"]


    callback_data_confirm = f"confirmcontract_{user_name}_{chat_id}"
    callback_data_reject = f"rejectcontractt"
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(
        text="✅ ثبت درخواست برای فعال شدن پس پرداخت",
        callback_data=callback_data_confirm,
    )
    button2 = InlineKeyboardButton(
        text="❌ رد کردن", callback_data=callback_data_reject
    )
    markup.add(button1, button2)
    price = traffic_price_query.show_price()
    dead_line = traffic_price_query.show_dead_line()
    bot.send_message(
        chat_id=chat_id,
        text=f"{messages_setting.DEBT_CONTRACT}\n💵قیمت تمام شده هرگیگ: {price} تومان\n📅مهلت پرداخت صورتحساب: {dead_line} روز\n",
        reply_markup=markup)
    


# callback handler
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("❌ بازگشت ❌"))

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "add_an_admin":
        bot.edit_message_text(text=messages_setting.ADD_ADMIN_STEP1, chat_id=chat_id, message_id=message_id)
        bot.register_next_step_handler(call.message, add_admin_step1)

    elif call.data == "modify_admin":
        bot.edit_message_text(
            text="یوزرنیم ادمین موردنظر رو وارد کنید:",
            chat_id=chat_id,
            message_id=message_id
        )
        bot.register_next_step_handler(call.message, modify_admin)

    elif call.data.startswith("change_inb_"):
        user_name = call.data.split("_")[2]
        bot.send_message(
            chat_id=chat_id,
            text=messages_setting.CHANGE_INB,
            reply_markup=markup
        )
        bot.register_next_step_handler(
            call.message, lambda msg: edit_inb_step1(msg, user_name))

    elif call.data.startswith("add_traffic_"):
        user_name = call.data.split("_")[2]
        bot.send_message(
            chat_id=chat_id,
            text="ترافیک مورد نظر رو به گیگابایت وارد کنید:",
            reply_markup=markup
        )
        bot.register_next_step_handler(
            call.message, lambda msg: add_traffic_step1(msg, user_name)
        )

    elif call.data.startswith("delete_admin_"):
        user_name = call.data.split("_")[2]
        bot.send_message(
            chat_id=chat_id,
            text="جهت حذف این نماینده کلمه [تایید] رو بفرستید:",
            reply_markup=markup
        )
        bot.register_next_step_handler(
            call.message, lambda msg: delete_admin(msg, user_name)
            )
        
    elif call.data.startswith("reduse_traffic_"):
        user_name = call.data.split("_")[2]
        bot.send_message(
            chat_id=chat_id,
            text="مقدار ترافیک جهت کاهش را به گیگابایت وارد کنید:",
            reply_markup=markup
        )
        bot.register_next_step_handler(
            call.message, lambda msg: reduse_traffic_by_admin(msg, user_name)
        )

    elif call.data.startswith("status_for_"):
        user_name = call.data.split("_")[2]
        admin = admins_query.admin_data_for_modify(user_name)
        current_status = admin["status"]
        new_status = not current_status
        if admins_query.change_admin_status(user_name, new_status):
            text = text_modify_admin(user_name)
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                parse_mode="HTML",
                reply_markup=admin_modify_control(user_name)
            )

    elif call.data == "add_a_plan":
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.send_message(chat_id=chat_id, text=messages_setting.ADD_PLAN_STEP1, reply_markup=markup)
        bot.register_next_step_handler(call.message, add_plan_step1)

    elif call.data == "change_plan":
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.send_message(chat_id=chat_id, text=messages_setting.CHANGE_PLAN_STEP1, reply_markup=markup)
        bot.register_next_step_handler(call.message, change_plan_step1)

    elif call.data == "delete_plan":
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.send_message(chat_id=chat_id, text=messages_setting.DELETE_PLAN, reply_markup=markup)
        bot.register_next_step_handler(call.message, delete_plan)

    elif call.data == "set_card":
        card = card_number_query.show_card()
        card = card["card_number"]
        msg = bot.send_message(
            chat_id,
            f"*💳 شماره حساب فعلی:\n{card}*\n\n ♻️ لطفا شماره حساب جدید خود را وارد کنید(با یا بدون نام صاحب حساب):",
            parse_mode="markdown",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, save_new_card_id)

    elif call.data == "login":
        bot.edit_message_text(
            text="لطفا یوزرنیم خود را وارد کنید:",
            chat_id=chat_id,
            message_id=message_id,
        )
        bot.register_next_step_handler(call.message, login_step1)

    elif call.data == "Register":
        registering_page(call)

    elif call.data.startswith("confirm_"):
        username = call.data.split("_")[1]
        name = call.data.split("_")[2]
        user_chat_id = call.data.split("_")[3]
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(
            user_chat_id, "♻️ درخواست ثبت نام شما ارسال شد، لطفا منتظر باشید..."
        )
        caption = (
            f"*🧾در خواست ثبت نام جدید!*\n\n"
            f"👤 *نام:* {name} \n"
            f"👤 *یوزرنیم:* @{username}\n"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        button1 = InlineKeyboardButton(
            text="✅ تایید", callback_data=f"accept_{user_chat_id}"
        )
        button2 = InlineKeyboardButton(
            text="❌ رد کردن", callback_data=f"rejectt_{user_chat_id}"
        )
        markup.add(button1, button2)

        bot.send_message(
            Admin_chat_id, caption, parse_mode="markdown", reply_markup=markup
        )

    elif call.data.startswith("rejectt_"):
        user_chat_id = call.data.split("_")[1]
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_chat_id, "🔴 درخواست ثبت نام شما رد شد.")

    elif call.data.startswith("accept_"):
        user_chat_id = call.data.split("_")[1]
        msg = bot.send_message(Admin_chat_id, messages_setting.CONFIRM_REGIST)
        bot.register_next_step_handler(msg, accept_register_step1, user_chat_id)

    elif call.data.startswith("reject_"):
        username = call.data.split("_")[1]
        name = call.data.split("_")[2]
        user_chat_id = call.data.split("_")[3]
        caption = (
            f"*⚠️ قوانین ثبت نام توسط کاربر زیر رد شد!*\n\n"
            f"👤 *نام:* {name} \n"
            f"👤 *یوزرنیم:* @{username}\n"
        )
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(user_chat_id, "❌شما قوانین را رد کردید\n➡️ /start ⬅️")
        bot.send_message(
            Admin_chat_id,
            caption,
            parse_mode="markdown",
            reply_markup=main_admin_menu(),
        )

    elif call.data.startswith("del_"):
        email = call.data.split("_")[1]
        bot.delete_message(call.message.chat.id, call.message.message_id)
        delete_user_step2(call, email)

    elif call.data.startswith("select_plan_"):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        id = call.data.split("_")[2]
        bot.send_message(
            chat_id=chat_id,
            text="🔗روش پرداخت خود را انتخاب کنید",
            reply_markup=payment_methods(),
        )
        data[chat_id] = id

    elif call.data == "card_payment":
        get_card = card_number_query.show_card()
        card = get_card["card_number"]
        bot.delete_message(call.message.chat.id, call.message.message_id)
        id = data.get(chat_id, "نامشخص")
        bot.send_message(
            chat_id=chat_id,
            text=f"*{messages_setting.CARD_PAYMENT_MESSAGE}\n💳 شماره کارت:*\n```{card}```",
            parse_mode="markdown",
        )
        bot.register_next_step_handler(call.message, receive_photo_step, id, chat_id)

    elif call.data == "card_payment_for_debt":
        get_card = card_number_query.show_card()
        card = get_card["card_number"]
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(
            chat_id=chat_id,
            text=f"*{messages_setting.CARD_PAYMENT_MESSAGE}\n💳 شماره کارت:*\n```{card}```",
            parse_mode="markdown",
        )
        bot.register_next_step_handler(call.message, receive_photo_step_for_debt, chat_id)

    elif call.data == "cancel":
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
        bot.send_message(chat_id, text="✅ عملیات لغو شد!", reply_markup=admins_menu())

    elif call.data == "change_start_notif_status":
        current_status = setting_query.show_start_notif()
        new_status = not current_status
        setting_query.change_start_notif(new_status)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=get_notif_status_text(),
            parse_mode="HTML",
            reply_markup=notif_status_menu(),
        )
    
    elif call.data == "change_create_notif_status":
        current_status = setting_query.show_create_notif()
        new_status = not current_status
        setting_query.change_create_notif(new_status)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=get_notif_status_text(),
            parse_mode="HTML",
            reply_markup=notif_status_menu()
        )

    elif call.data == "change_delete_notif_status":
        current_status = setting_query.show_delete_notif()
        new_status = not current_status
        setting_query.change_delete_notif(new_status)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=get_notif_status_text(),
            parse_mode="HTML",
            reply_markup=notif_status_menu(),
        )

    elif call.data == "change_debt_status":
        current_status = setting_query.show_debt_stasus()
        new_status = not current_status
        setting_query.change_debt_system(new_status)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=debt_status_text(),
            parse_mode="HTML",
            reply_markup=debt_control()
        )
    
    elif call.data == "change_debt_price":
        current_price = traffic_price_query.show_price()
        text = (
            f"<b>💸 قیمت فعلی برای هر 1 گیگ: {current_price}</b>\n\n"
            f"قیمت جدید را به تومان وارد گنید:"
        )
        bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
        bot.register_next_step_handler(call.message, change_debt_price)

    elif call.data == "dead_line":
        current_dead_line = traffic_price_query.show_dead_line()
        text = (
            f"<b>⌛ مهلت پرداخت صورتحساب فعلی: {current_dead_line} روز</b>\n\n"
            f"مهلت پرداخت جدید را به عدد وارد کنید:"
        )
        bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
        bot.register_next_step_handler(call.message, change_dead_line)

    elif call.data.startswith("confirmcontract_"):
        username = call.data.split("_")[1]
        user_chat_id = call.data.split("_")[2]
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(
            user_chat_id, "♻️ درخواست شما ارسال شد، لطفا منتظر باشید..."
        )
        caption = (
            f"*💸در خواست فعال سازی پس پرداخت !*\n\n"
            f"👤 *نماینده:* {username} \n"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        button1 = InlineKeyboardButton(
            text="✅ تایید", callback_data=f"acceptcontract_{user_chat_id}"
        )
        button2 = InlineKeyboardButton(
            text="❌ رد کردن", callback_data=f"rejectcontract_{user_chat_id}"
        )
        markup.add(button1, button2)

        bot.send_message(
            Admin_chat_id, caption, parse_mode="markdown", reply_markup=markup
        )
    
    elif call.data.startswith("acceptcontract_"):
        user_chat_id = call.data.split("_")[1]
        dead_line = traffic_price_query.show_dead_line()
        if admins_query.set_debt_system(user_chat_id, "false", 0, dead_line):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(
                user_chat_id, "✅ درخواست شما برای متود پس پرداخت تایید شد، برای اطلاعات بیشتر و پرداخت صورت حساب به بخش مشخصات من مراجعه کنید."
            )
            bot.send_message(
                Admin_chat_id, "✅ درخواست نماینده برای متود پس پرداخت تایید شد"
            )
            

    elif call.data.startswith("rejectcontract_"):
        user_chat_id = call.data.split("_")[1]
        bot.send_message(
            user_chat_id, "❌ درخواست شما برای متود پس پرداخت رد شد."
        )
        bot.send_message(
            Admin_chat_id, "❌ درخواست نماینده برای متود پس پرداخت رد شد"
        )
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif call.data == "rejectcontractt":
        bot.delete_message(call.message.chat.id, call.message.message_id)


def change_debt_price(message):
    try:
        new_price = message.text
        if traffic_price_query.add_price(new_price):
            caption = (
                f"✅ قیمت جدید ثبت شد\n"
                f"قیمت هر گیگ: {new_price}"
            )
            bot.send_message(
                message.chat.id,
                caption,
                reply_markup=setting_menu()
            )
    except:
        pass

def change_dead_line(message):
    try:
        new_dead_line = int(message.text)
        if traffic_price_query.add_dead_line(new_dead_line):
            caption = (
                f"⌛ مهلت پرداخت جدید ثبت شد"
            )
            bot.send_message(
                message.chat.id,
                caption,
                reply_markup=setting_menu()
            )
    except:
        pass


# add plan
def add_plan_step1(message):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات ویرایش راهنما لغو شد.",
            reply_markup=main_admin_menu(),
        )
    try:
        traffic = message.text
        bot.send_message(message.chat.id, messages_setting.ADD_PLAN_STEP2)
        bot.register_next_step_handler(
            message, lambda msg: add_plan_step2(msg, traffic)
        )
    except ValueError:
        bot.send_message(message.chat.id, "❌ Please send a valid world.")


def add_plan_step2(message, traffic):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات ویرایش راهنما لغو شد.",
            reply_markup=main_admin_menu(),
        )
    try:
        price = message.text
        added_plan = price_query.add_plan(traffic, price)
        if added_plan:
            bot.send_message(
                message.chat.id,
                "✅پلن شما با موفقیت ساخته شد",
                reply_markup=main_admin_menu(),
            )
    except ValueError:
        bot.send_message(message.chat.id, "❌ Please send a valid world.")


# change plan
def change_plan_step1(message):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات ویرایش راهنما لغو شد.",
            reply_markup=setting_menu(),
        )
    try:
        id = message.text
        bot.send_message(message.chat.id, messages_setting.CHANGE_PLAN_STEP2)
        bot.register_next_step_handler(message, lambda msg: change_plan_step2(msg, id))
    except ValueError:
        bot.send_message(message.chat.id, "❌ Please send a valid world.")


def change_plan_step2(message, id):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات ویرایش راهنما لغو شد.",
            reply_markup=setting_menu(),
        )
    try:
        traffic = message.text
        bot.send_message(message.chat.id, messages_setting.CHANGE_PLAN_STEP3)
        bot.register_next_step_handler(
            message, lambda msg: change_plan_step3(msg, id, traffic)
        )
    except ValueError:
        bot.send_message(message.chat.id, "❌ Please send a valid world.")


def change_plan_step3(message, id, traffic):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات ویرایش راهنما لغو شد.",
            reply_markup=setting_menu(),
        )
    try:
        price = message.text
        if price_query.edite_plan(id, traffic, price):
            bot.send_message(
                message.chat.id,
                "✅تغییرات با موفقیت اعمال شد",
                reply_markup=setting_menu(),
            )
        else:
            bot.send_message(
                message.chat.id,
                "❌ مقادریر واردشده صحیح نیستن\n(از صحت ایدی پلن اطمینان حاصل کنید!!)",
                reply_markup=setting_menu(),
            )
    except ValueError:
        bot.send_message(message.chat.id, "❌ Please send a valid world.")


# delete plan
def delete_plan(message):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id, "✅ عملیات  لغو شد.", reply_markup=main_admin_menu()
        )
    try:
        id = message.text
        if price_query.delete_plan(id):
            bot.send_message(
                message.chat.id, "✅پلن مورد نظر حذف شد", reply_markup=main_admin_menu()
            )
        else:
            msg = bot.send_message(message.chat.id, "❌ لطفا یک عدد درست ارسال کنید.")
            bot.register_next_step_handler(msg, delete_plan)

    except ValueError:
        bot.send_message(message.chat.id, "❌ Please send a valid world.")

# modify admin 
def text_modify_admin(user_name):
    admin = admins_query.admin_data_for_modify(user_name)
    admin_debt_traffic = admin["debt"]
    price = traffic_price_query.show_price()
    debt = admin_debt_traffic * price  
        
    traffic = admin['traffic']
    if traffic == "false":
        traffic = 0

    status = admin['status']
    if status:
        status = "فعال"
    else:
        status = "غیر فعال"

    login_status = admin['chat_id'] 
    if login_status is None:
        login_status = "لاگین نشده/ خارج شده"
    else:
        login_status = "لاگین شده"

    text = (
        f"<b>✓ مشخصات نماینده</b>\n\n"
        f"<b>👤 یوزرنیم:</b> {admin['user_name']}\n"
        f"<b>🔐 پسورد:</b> {admin['password']}\n"
        f"<b>🛜 وضعیت:</b> {status}\n"
        f"<b>💻 وضعیت لاگین:</b> {login_status}\n"
        f"<b>🔢 اینباند درحال استفاده:</b> {admin['inb_id']}\n"
        f"<b>📊 ترافیک باقی‌مانده:</b> {traffic} GB\n"
        f"<b>💸 بدهی:</b> {debt} تومان\n"
        f"<b>📅 مهلت پرداخت بدهی:</b> {admin['debt_days']} روز\n"
    )
    return text
    
def modify_admin(message):
    user_name = message.text
    if admins_query.approv_for_modify(user_name):
        text = text_modify_admin(user_name)
        bot.send_message(
            message.chat.id,
            text=text,
            parse_mode="HTML",
            reply_markup=admin_modify_control(user_name)
        )
    else:
        bot.send_message(
            message.chat.id,
            text="❌ یوزرنیم وارد شده در دیتابیس وجود ندارد"
        )

# add admin func
def add_admin_step1(message):
    if message.content_type == "text":
        try:
            user_name = message.text
            bot.send_message(message.chat.id, messages_setting.ADD_ADMIN_STEP2)
            bot.register_next_step_handler(
                message, lambda msg: add_admin_step2(msg, user_name)
            )
        except ValueError:
            bot.send_message(message.chat.id, "❌ Please send a valid world.")


def add_admin_step2(message, user_name):
    if message.content_type == "text":
        try:
            password = message.text
            bot.send_message(message.chat.id, messages_setting.ADD_ADMIN_STEP3)
            bot.register_next_step_handler(
                message, lambda msg: add_admin_step3(msg, user_name, password)
            )
        except ValueError:
            bot.send_message(message.chat.id, "❌ Please send a valid world.")


def add_admin_step3(message, user_name, password):
    if message.content_type == "text":
        try:
            traffic = int(message.text)
            bot.send_message(message.chat.id, messages_setting.ADD_ADMIN_STEP4)
            bot.register_next_step_handler(
                message, lambda msg: add_admin_step4(msg, user_name, password, traffic)
            )
        except ValueError:
            bot.send_message(message.chat.id, "❌ Please send a valid world.")


def add_admin_step4(message, user_name, password, trafiic):
    if message.content_type == "text":
        try:
            inb_id = int(message.text)
            if admins_query.add_admin(user_name, password, trafiic, inb_id):
                bot.send_message(
                    message.chat.id,
                    f"✅ ادمین اضافه شد: \n👤username: {user_name} \n🔐password: {password} \n🔋total trafiic: {trafiic}",
                    reply_markup=main_admin_menu(),
                )
            else:
                bot.send_message(message.chat.id, "admin already exists.")
        except ValueError:
            bot.send_message(message.chat.id, "❌ Please send a valid number.")


# add traffic
def add_traffic_step1(message, user_name):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات ویرایش راهنما لغو شد.",
            reply_markup=main_admin_menu(),
        )
    else:
        try:
            traffic = int(message.text)
        except ValueError:
            bot.send_message(
                message.chat.id,
                "❌ لطفاً یک عدد معتبر وارد کنید.",
            )
            return bot.register_next_step_handler(message, lambda msg: add_traffic_step1(msg, user_name))
            

        if admins_query.add_traffic(user_name, traffic):
            bot.send_message(
                message.chat.id,
                "✅ ترافیک با موفقیت اضافه شد",
                reply_markup=main_admin_menu()
            )
        else:
            bot.send_message(
                message.chat.id,
                "❌ نماینده با این نام پیدا نشد ",
                reply_markup=main_admin_menu()
            )

# reduse traffic
def reduse_traffic_by_admin(message, user_name):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات ویرایش راهنما لغو شد.",
            reply_markup=main_admin_menu(),
        )
    else:
        try:
            r_traffic = int(message.text)
        except ValueError:
            bot.send_message(
                message.chat.id,
                "❌ لطفاً یک عدد معتبر وارد کنید.",
            )
            return bot.register_next_step_handler(message, lambda msg: reduse_traffic_by_admin(msg, user_name))
        if admins_query.reduse_traffic_by_username(user_name, r_traffic):
            bot.send_message(
                message.chat.id,
                "✅ترافیک مورد نظر باموفقیت کاهش یافت",
                reply_markup=main_admin_menu()
            )
        else:
            bot.send_message(
                message.chat.id,
                "❌خطا:\nنماینده مورد نظر در پلن پس پرداخت فعال است و ترافیکی ندارد",
                reply_markup=main_admin_menu()
            )

# edit inb id
def edit_inb_step1(message, user_name):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات ویرایش راهنما لغو شد.",
            reply_markup=main_admin_menu(),
        )
    else:
        try:
            new_inb = int(message.text)
        except ValueError:
            bot.send_message(
                message.chat.id,
                "❌ لطفاً یک عدد معتبر وارد کنید.",
            )
            return bot.register_next_step_handler(message, lambda msg: edit_inb_step1(msg, user_name))

        if admins_query.change_inb(user_name, new_inb):
            bot.send_message(
                message.chat.id,
                f"✅ اینباند ( {user_name} ) به {new_inb} تغییر یافت",
                reply_markup=main_admin_menu()
            )



# del admins
def delete_admin(message, user_name):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات ویرایش راهنما لغو شد.",
            reply_markup=main_admin_menu(),
        )
    if message.text == "تایید":
        admins_query.delete_admin(user_name)
        bot.send_message(
            message.chat.id,
            f"✅ ادمین با یوزرنیم: [{user_name}] حذف شد ",
            reply_markup=main_admin_menu()
        )
    else:
        bot.send_message(
            message.chat.id,
            "⚠️ اگه تایید نمیکنید لطفا دکمه بازگشت رو بزنید",
            )
        return bot.register_next_step_handler(message, lambda msg: delete_admin(msg, user_name))
    
    
    



# login
def login_step1(message):
    if message.content_type == "text":
        try:
            user_name = message.text
            bot.send_message(message.chat.id, "حالا پسورد خود را وارد کنید:")
            bot.register_next_step_handler(
                message, lambda msg: login_step2(msg, user_name)
            )
        except ValueError:
            bot.send_message(message.chat.id, "Please enter a valid world.")


def login_step2(message, user_name):
    if message.content_type == "text":
        try:
            password = message.text
            chat_id = message.chat.id
            if admins_query.add_chat_id(user_name, password, chat_id):
                bot.send_message(
                    message.chat.id,
                    f"*{messages_setting.START_NONE_SUDO}*",
                    parse_mode="markdown",
                    reply_markup=admins_menu(),
                )
            else:
                bot.send_message(
                    message.chat.id, "❌  /start .پسورد یا نام کاربری اشتباه است."
                )
        except ValueError:
            bot.send_message(message.chat.id, "Please enter a valid world.")


# add user to panel
user_email = {}
user_days = {}
user_gb = {}


def add_user_step1(message):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات ویرایش راهنما لغو شد.",
            reply_markup=admins_menu(),
        )
    else:
        try:
            chat_id = message.chat.id
            email = str(message.text).strip()
            random_numb = random.randint(10, 99)
            user_email[chat_id] = f"{email}{random_numb}"
            bot.send_message(chat_id, messages_setting.ADD_USER_STEP2)
            bot.register_next_step_handler(message, add_user_step2)
        except Exception as e:
            bot.send_message(message.chat.id, f"Error: {e}")


def add_user_step2(message):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات ویرایش راهنما لغو شد.",
            reply_markup=admins_menu(),
        )
    else:
        chat_id = message.chat.id
        try:
            days = int(message.text)
            user_days[chat_id] = days
            bot.send_message(chat_id, messages_setting.ADD_USER_STEP3)
            bot.register_next_step_handler(message, add_user_step3)
        except ValueError:
            bot.send_message(
                chat_id, "Invalid input. Please enter a valid number for days."
            )
            bot.register_next_step_handler(message, add_user_step2)


def add_user_step3(message):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات لغو شد.",
            reply_markup=admins_menu(),
        )

    chat_id = message.chat.id
    try:
        admin_data = admins_query.admin_data(chat_id)
        admin_traffic = admin_data["traffic"]
        gb = message.text.strip()

        if not gb.isdigit() or int(gb) <= 0:
            bot.send_message(chat_id, "❌ لطفاً مقدار ترافیک معتبر و مثبت وارد کنید.")
            bot.register_next_step_handler(message, add_user_step3)
            return

        gb = int(gb)


        if admin_traffic.lower() == "false":
            admin_traffic = False
        else:
            try:
                admin_traffic = int(admin_traffic)
            except ValueError:
                bot.send_message(chat_id, "❌ مقدار ترافیک نامعتبر است، لطفاً دوباره امتحان کنید.")
                return


        if admin_traffic is False:
            success = admins_query.reduce_traffic(chat_id, gb)

        else:
            if gb > admin_traffic:
                bot.send_message(
                    chat_id,
                    f"❌ ترافیک کافی برای ایجاد کاربر ندارید. (ترافیک شما: {admin_traffic} GB)",
                    reply_markup=admins_menu(),
                )
                return

            if admin_traffic < 100:
                warning_text = (
                    "⚠️ *هشدار مهم*\n\n"
                    "🚨 *ترافیک باقی‌مانده شما کمتر از 100 گیگ است!*\n"
                )
                bot.send_message(chat_id, warning_text, parse_mode="Markdown")

            success = admins_query.reduce_traffic(chat_id, gb)

        if success:
            user_gb[chat_id] = gb
            add_user_f(chat_id)
        else:
            bot.send_message(chat_id, "❌ مشکلی در به‌روزرسانی ترافیک پیش آمد.")

    except Exception as e:
        bot.send_message(
            chat_id, "❌ مقدار وارد شده صحیح نیست. لطفاً یک عدد معتبر وارد کنید."
        )
        bot.register_next_step_handler(message, add_user_step3)



def generate_secure_random_text(length=16):
    characters = string.ascii_letters + string.digits
    secure_text = "".join(secrets.choice(characters) for _ in range(length))
    return secure_text


def add_user_f(chat_id):
    email = user_email.get(chat_id)
    days = user_days.get(chat_id)
    gb = user_gb.get(chat_id)

    bytes_value = int(gb * 1024 * 1024 * 1024)
    expiry_time = int(
        (datetime.datetime.now() + datetime.timedelta(days=days)).timestamp() * 1000
    )
    sub_id = generate_secure_random_text(16)
    c_uuid = str(uuid.uuid4())
    get = admins_query.admin_data(chat_id)
    inb_id = get["inb_id"]
    request = api.add_user(c_uuid, email, bytes_value, expiry_time, sub_id, inb_id)

    if request:
        sub_url = f"https://{sub}/{sub_id}"
        qr = sub_url
        img = segno.make(qr)
        img.save("last_qrcode.png", scale=10, dark="darkblue", data_dark="steelblue")
        img_path = "last_qrcode.png"
        caption_text = (
            f"🪪<b>نام کاربری:  </b>{user_email[chat_id]}\n"
            f"⌛<b>تعداد روز:  </b>{user_days[chat_id]}\n"
            f"🔋<b>سقف ترافیک:  </b>{gb} GB\n\n"
            f"🔗<b>لینک سابسکریپشن:</b>\n"
            f"<code>\n{sub_url}\n</code>"
        )

        with open(img_path, "rb") as photo:
            bot.send_photo(
                chat_id,
                photo,
                caption=caption_text,
                parse_mode="HTML",
                reply_markup=admins_menu(),
            )
        if setting_query.show_create_notif():
            admin_data = admins_query.admin_data(chat_id)
            admin_name = admin_data["user_name"]
            notif_setting.create_notif(email, admin_name, days, gb)
        clear_user_data(chat_id)
    else:
        bot.send_message(
            chat_id,
            f"Failed to add user. Error: {request.text}",
            reply_markup=admins_menu(),
        )


def clear_user_data(chat_id):
    user_email.pop(chat_id, None)
    user_days.pop(chat_id, None)
    user_gb.pop(chat_id, None)


# get info
def get_admin_info(chat_id):
    get_status = admins_query.admin_data(chat_id)  
    user_status = get_status["traffic"]
    username = get_status["user_name"]
    password = get_status["password"]
    
    if user_status.lower() == "false":
        get_admin_debt = admins_query.admin_data(chat_id)
        admin_debt_traffic = get_admin_debt["debt"]
        admin_dead_line = get_admin_debt["debt_days"]
        price = traffic_price_query.show_price()
        debt = admin_debt_traffic * price

        caption = (
            f"🔗* مشخصات شما*\n\n"
            f"👤* یوزرنیم:*  {username}\n"
            f"🔐* پسورد:*  {password}\n"
            f"💸* بدهی شما:*  {debt} تومان\n"
            f"📅* مهلت پرداخت صورتحساب:*  {admin_dead_line} روز\n"

        )
        bot.send_message(
            chat_id, caption, parse_mode="markdown", reply_markup=payment_methods_for_debt()
        )

    else:
        admin_traffic = get_status["traffic"]
        caption = (
            f"🔗* مشخصات شما*\n\n"
            f"👤* یوزرنیم:*  {username}\n"
            f"🔐* پسورد:*  {password}\n"
            f"🔋* ترافیک باقی مانده:*  {admin_traffic} GB\n\n"
        )
        bot.send_message(
            chat_id, caption, parse_mode="markdown", reply_markup=admins_menu()
        )


# show clients
email_data = {}


def cancel_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("❌ بازگشت ❌"))
    return markup


def send_emails_(chat_id):
    get_admin_inb_id = admins_query.admin_data(chat_id)
    inb_id = get_admin_inb_id["inb_id"]
    get = api.show_users(inb_id)
    if get:
        try:
            data = get.json()
        except requests.exceptions.JSONDecodeError:
            os._exit(1)
            return
        try:
            settings = json.loads(data["obj"]["settings"])
            clients = settings["clients"]
        except:
            return bot.send_message(
                chat_id, "⚠️ در مقادیر اشتراک شما مشکلی هست!", reply_markup=admins_menu()
            )

        if not clients:
            bot.send_message(chat_id, "No users found.")
            os._exit(1)
            return

        number_to_emoji = {
            0: "0️⃣",
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            5: "5️⃣",
            6: "6️⃣",
            7: "7️⃣",
            8: "8️⃣",
            9: "9️⃣",
        }

        def number_to_emoji_string(number):
            return "".join(number_to_emoji[int(digit)] for digit in str(number))

        user_list = "📋* لیست کاربران:*\n\n"
        for index, client in enumerate(clients, start=1):
            email = client.get("email", "Unknown")
            expiry_time = client.get("expiryTime", 0)
            remaining_days = 0

            get_traffic = api.user_obj(email)
            response = get_traffic.json()
            obj = response.get("obj", {})
            uploaded = obj.get("up")
            downloaded = obj.get("down")
            total_bytes = obj.get("total")
            traffic = (uploaded + downloaded) / (1024**3)
            current_traffic = total_bytes / (1024**3) - traffic


            if expiry_time > 0:
                current_time = int(time.time() * 1000)
                remaining_time_ms = expiry_time - current_time
                if remaining_time_ms > 0:
                    remaining_days = int(remaining_time_ms / (1000 * 60 * 60 * 24))

            user_list += "```"
            index_emoji = number_to_emoji_string(index)
            user_list += f"\n{index_emoji}| 👤 {email}    ⌛ = {remaining_days}  🔋 = {int(current_traffic)} GB \n\n"
            user_list += "```"
            if len(user_list) > 3500:
                bot.send_message(
                    chat_id,
                    user_list,
                    parse_mode="Markdown",
                    reply_markup=cancel_button(),
                )
                user_list = ""

        user_list += "\n📩 شماره کاربر مورد نظر رو جهت دریافت اطلاعات وارد کنید:"
        bot.send_message(
            chat_id, user_list, parse_mode="Markdown", reply_markup=cancel_button()
        )

        email_data[chat_id] = clients

        bot.register_next_step_handler_by_chat_id(chat_id, send_sub_id)
    else:
        bot.send_message(
            chat_id, f"Failed to fetch user list. Status code: {get.status_code}"
        )


# send user info
def send_sub_id(message):
    chat_id = message.chat.id

    if message.text == "❌ بازگشت ❌":
        bot.send_message(chat_id, "✅ عملیات لغو شد.", reply_markup=admins_menu())
        return

    if not message.text.isdigit():
        bot.send_message(
            chat_id, "❌ لطفاً فقط عدد وارد کنید.", reply_markup=cancel_button()
        )
        bot.register_next_step_handler(message, send_sub_id)
        return

    user_index = int(message.text) - 1

    if (
        chat_id not in email_data
        or user_index < 0
        or user_index >= len(email_data[chat_id])
    ):
        bot.send_message(
            chat_id,
            "❌ شماره وارد شده معتبر نیست. لطفاً دوباره امتحان کنید.",
            reply_markup=cancel_button(),
        )
        bot.register_next_step_handler(message, send_sub_id)
        return

    selected_user = email_data[chat_id][user_index]
    email = selected_user.get("email", "Unknown")
    sub_id = selected_user.get("subId", "Sub ID not found")

    get = api.user_obj(email)

    if get.status_code == 200:
        response = get.json()
        sub_url = f"https://{sub}/{sub_id}"
        qr = sub_url
        img = segno.make(qr)
        img.save("last_qrcode.png", scale=10, dark="darkblue", data_dark="steelblue")
        img_path = "last_qrcode.png"

        obj = response.get("obj", {})
        user_id = obj.get("id")
        # status = obj.get('enable')
        uploaded = obj.get("up")
        downloaded = obj.get("down")
        expiry_time = obj.get("expiryTime")
        total_bytes = obj.get("total")

        usage_traffic = (uploaded + downloaded) / (1024**3)
        total_traffic = total_bytes / (1024**3)

        # expiry_time
        expiry_time_s = expiry_time / 1000
        expiry_date = datetime.datetime.fromtimestamp(expiry_time_s)
        current_time = datetime.datetime.now()
        remaining_time = expiry_date - current_time
        remaining_days = remaining_time.days

        caption_text = (
            f"🪪 <b>نام کاربری:</b> {email}\n"
            f"⌛ <b>روزهای باقی مانده:</b> {remaining_days}\n"
            f"🔋 <b>ترافیک مصرف شده:</b> {usage_traffic:.2f} GB\n"
            f"📦 <b>کل ترافیک:</b> {total_traffic:.2f} GB\n\n"
            f"🔗 <b>لینک سابسکریپشن:</b>\n"
            f"<code>{sub_url}</code>"
        )

        with open(img_path, "rb") as photo:
            bot.send_photo(
                chat_id,
                photo,
                caption=caption_text,
                parse_mode="HTML",
                reply_markup=admins_menu(),
            )


# renew user
def renew_user_step1(message):
    if message.text.strip() in ["❌ بازگشت ❌"]:
        bot.send_message(
            message.chat.id, "✅ عملیات لغو شد!", reply_markup=admins_menu()
        )
        return

    email = message.text
    chat_id = message.chat.id

    get = api.user_obj(email)

    if get.status_code == 200:
        try:
            response = get.json()
        except Exception as e:
            bot.send_message(
                chat_id,
                "❌ خطا در پردازش پاسخ از سرور!",
                parse_mode="markdown",
                reply_markup=admins_menu(),
            )
            return

        obj = response.get("obj")
        if obj is None:
            bot.send_message(
                chat_id,
                "❌ کاربر یافت نشد یا اطلاعات نامعتبر است!",
                parse_mode="markdown",
                reply_markup=admins_menu(),
            )
            return

        gb = obj.get("total", 0) / (1024**3)
        get_admin_traffic = admins_query.admin_data(chat_id)
        admin_traffic = get_admin_traffic["traffic"]
        if admins_query != "false":
            try:
                if gb > admin_traffic:
                    bot.send_message(
                        chat_id,
                        f"❌ ترافیک کافی برای ایجاد کاربر ندارید. (ترافیک شما: {admin_traffic} GB)",
                        reply_markup=admins_menu(),
                    )
                    return

                if admin_traffic < 100:
                    warning_text = (
                        "⚠️ *هشدار مهم*\n\n"
                        "🚨 *ترافیک باقی‌مانده شما کمتر از 100 گیگ است!*\n"
                        "❗ لطفاً بررسی کنید."
                    )
                    bot.send_message(chat_id, warning_text, parse_mode="Markdown")
            except:
                pass

        if admins_query.reduce_traffic(chat_id, gb):
            get_admin_inb_id = admins_query.admin_data(chat_id)
            inb_id = get_admin_inb_id["inb_id"]

            response = api.reset_traffic(inb_id, email)
            if response.status_code == 200:
                bot.send_message(
                    chat_id,
                    "*✅ ترافیک کاربر ریست شد، حالا تعداد روز تمدید رو واردکنید:*",
                    parse_mode="markdown",
                )
                bot.register_next_step_handler(
                    message, lambda msg: renew_user_step2(msg, email)
                )
    else:
        bot.send_message(
            chat_id,
            "*❌ درخواست با خطا مواجه شد، لطفاً بعداً تلاش کنید!*",
            parse_mode="markdown",
            reply_markup=admins_menu(),
        )


# renew user step2
def renew_user_step2(message, email):
    if message.text.strip() in ["❌ بازگشت ❌"]:
        bot.send_message(
            message.chat.id, "✅ عملیات لغو شد!", reply_markup=admins_menu()
        )
        return

    try:
        days = int(message.text)
    except ValueError:
        bot.send_message(
            message.chat.id,
            "❌ لطفاً یک عدد معتبر وارد کنید.",
            reply_markup=admins_menu(),
        )
        return

    chat_id = message.chat.id
    expiry_time = int(
        (datetime.datetime.now() + datetime.timedelta(days=days)).timestamp() * 1000
    )
    get = api.user_obj(email)

    if get.status_code == 200:
        get_admin_inb_id = admins_query.admin_data(chat_id)
        inb_id = get_admin_inb_id["inb_id"]
        response = api.get_inbound(inb_id)

        if response.status_code == 200:
            data = response.json()
            settings = json.loads(data["obj"]["settings"])
            clients = settings["clients"]

            for client in clients:
                if client["email"] == email:
                    id = client["id"]
                    total_gb = client["totalGB"]
                    sub_id = client["subId"]
                    break

            settings = {
                "clients": [
                    {
                        "id": id,
                        "enable": True,
                        "flow": "",
                        "email": email,
                        "imitIp": "",
                        "totalGB": total_gb,
                        "expiryTime": expiry_time,
                        "tgId": "",
                        "subId": sub_id,
                        "reset": "",
                    }
                ]
            }

            proces = {"id": inb_id, "settings": json.dumps(settings)}
            res = api.update_email(id, proces)

            if res.status_code == 200:
                bot.send_message(
                    chat_id,
                    f"*✅ اشتراک کاربر: {email}، با موفقیت تمدید شد*",
                    parse_mode="markdown",
                    reply_markup=admins_menu(),
                )
            else:
                bot.send_message(
                    chat_id,
                    f"*❌ خطا در تمدید: {res.status_code}*",
                    parse_mode="markdown",
                    reply_markup=admins_menu(),
                )
        else:
            bot.send_message(
                chat_id,
                f"*❌ خطا در دریافت اطلاعات کلاینت: {response.status_code}*",
                parse_mode="markdown",
                reply_markup=admins_menu(),
            )
    else:
        bot.send_message(
            chat_id,
            f"*❌ خطا در دریافت `inb_id`: {get.status_code}*",
            parse_mode="markdown",
            reply_markup=admins_menu(),
        )


# get users uuid and...
def get_users_info_by_email(email, chat_id):
    get_admin_inb_id = admins_query.admin_data(chat_id)
    inb_id = get_admin_inb_id["inb_id"]
    response = api.get_inbound(inb_id)

    if response.status_code == 200:
        data = response.json()

        if data.get("obj") is not None and "settings" in data["obj"]:
            settings = json.loads(data["obj"]["settings"])
            clients = settings.get("clients", [])

            for client in clients:
                if client.get("email") == email:
                    user_id = client.get("id")
                    # total_gb = client.get("totalGB")
                    # sub_id = client.get("subId")
                    return user_id
            return "not_found"


# delete user
def delete_user_step1(message):
    chat_id = message.chat.id
    if message.text == "❌ بازگشت ❌":
        bot.send_message(
            message.chat.id, "✅ عملیات لغو شد!", reply_markup=admins_menu()
        )
        return

    else:
        email = message.text
        callback_data = f"del_{email}"

        markup = InlineKeyboardMarkup(row_width=1)
        button1 = InlineKeyboardButton(text="✅ تایید ✅", callback_data=callback_data)
        button2 = InlineKeyboardButton(text="❌ لغو ❌", callback_data="cancel")
        markup.add(button1, button2)
        bot.send_message(
            chat_id,
            f"*⚠️شما درحال حذف [ {email} ] هستید.\nتایید میکنید؟*",
            parse_mode="markdown",
            reply_markup=markup,
        )


def delete_user_step2(call, email):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    user_id = get_users_info_by_email(email, chat_id)
    get_admin_inb_id = admins_query.admin_data(chat_id)
    inb_id = get_admin_inb_id["inb_id"]

    response = api.delete_user(inb_id, user_id)
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

    if user_id == "not_found":
        bot.send_message(
            chat_id=chat_id,
            text="*❌ خطا در دریافت اطلاعات کاربر.\n(کاربر وجود ندارد)*",
            parse_mode="markdown",
            reply_markup=admins_menu(),
        )
        return
    else:
        if response.status_code == 200:
            if setting_query.show_delete_notif():
                admin_data = admins_query.admin_data(chat_id)
                admin_name = admin_data["user_name"]
                notif_setting.delete_notif(admin_name, email)

            bot.send_message(
                chat_id=chat_id,
                text=f"*✅ کاربر {email} با موفقیت حذف شد.*",
                parse_mode="markdown",
                reply_markup=admins_menu(),
            )


# save new help message
def save_new_help_message(message):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات ویرایش راهنما لغو شد.",
            reply_markup=setting_menu(),
        )

    new_text = message.text.strip()
    if help_message_query.add_message(new_text):
        bot.send_message(
            message.chat.id,
            "✅متن راهنما با موفقیت تغییر یافت.",
            reply_markup=setting_menu(),
        )

    else:
        bot.send_message(
            message.chat.id, "خطا هنگام نوشتن در فایل", reply_markup=setting_menu()
        )


# save new card numb
def save_new_card_id(message):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات ویرایش راهنما لغو شد.",
            reply_markup=setting_menu(),
        )

    new_card = message.text.strip()
    if card_number_query.add(new_card):
        bot.send_message(
            message.chat.id,
            "✅شماره حساب با موفقیت تغییر یافت",
            reply_markup=setting_menu(),
        )

    else:
        bot.send_message(
            message.chat.id, "خطا هنگام نوشتن در فایل", reply_markup=setting_menu()
        )


# registering
def registering_page(call):
    register = registering_message.show_message()
    register = register["message"]
    chat_id = call.message.chat.id
    username = call.from_user.username
    name = call.from_user.first_name

    callback_data_confirm = f"confirm_{username}_{name}_{chat_id}"
    callback_data_reject = f"reject_{username}_{name}_{chat_id}"
    markup = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(
        text="✅ تایید قوانین و ثبت درخواست ثبت نام",
        callback_data=callback_data_confirm,
    )
    button2 = InlineKeyboardButton(
        text="❌ رد کردن قوانین", callback_data=callback_data_reject
    )
    markup.add(button1, button2)

    bot.send_message(chat_id=chat_id, text=register, reply_markup=markup)


# save new registering message
def save_new_register_message(message):
    if message.text == "❌ بازگشت ❌":
        return bot.send_message(
            message.chat.id,
            "✅ عملیات ویرایش راهنما لغو شد.",
            reply_markup=main_admin_menu(),
        )

    new_text = message.text.strip()
    if registering_message.add_message(new_text):
        bot.send_message(
            message.chat.id,
            "✅ متن ثبت نام باموفقیت تغییر یافت",
            reply_markup=main_admin_menu(),
        )


# accept registering step1
def accept_register_step1(message, user_chat_id):
    username = message.text
    bot.send_message(
        Admin_chat_id,
        "2️⃣مرحله دوم\nحالا پسورد اختصاصی این نماینده را به انگلیسی ارسال کنید:",
    )
    bot.register_next_step_handler(
        message, lambda msg: accept_register_step2(msg, user_chat_id, username)
    )


def accept_register_step2(message, user_chat_id, username):
    password = message.text
    bot.send_message(
        Admin_chat_id,
        "3️⃣مرحله سوم\nحالا عدد اینباند مختص این نماینده رو وارد کنید:\n(توجه کنید که اینباند خالی باشه و نماینده دیگری روی اون فعال نباشه)",
    )
    bot.register_next_step_handler(
        message,
        lambda msg: accept_register_step3(msg, user_chat_id, username, password),
    )


def accept_register_step3(message, user_chat_id, username, password):
    traffic = 0
    inb_id = int(message.text)
    if admins_query.add_admin(username, password, traffic, inb_id):
        bot.send_message(
            Admin_chat_id,
            "✅ اطلاعات در دیتابیس اضافه و به نماینده ارسال شد",
            reply_markup=main_admin_menu(),
        )
        caption = (
            f"*✅در خواست ثبت نام شما تایید شد!*\n\n"
            f"👤 *یوزنیم* {username} \n"
            f"🔑 *پسورد:* {password}\n➡️ /start  ⬅️"
        )
        bot.send_message(user_chat_id, caption, parse_mode="markdown")
    else:
        bot.send_message(
            Admin_chat_id,
            "❌ خطا در افزودن اطلاعات به دیتابیس!",
            reply_markup=main_admin_menu(),
        )

# backup page
def backup_page(message):
    bot.send_message(
        message.chat.id,
        text="🗂 وارد منوی پشتیبان گیری و بازگردانی دیتابیس وال بات شدید.",
        reply_markup=backup_menu()
    )
