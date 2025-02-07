from db.query import admins_query, price_query
from keyboards.keyboards import admins_menu
from messages.messages import *
from config import bot, Admin_chat_id
from telebot.types import InlineKeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from api import *

pending_payments = {}
def receive_photo_step(message, id, chat_id):
    if message.content_type == 'photo':
        get_username = admins_query.admin_data(chat_id)
        user_name = get_username['user_name']

        get_plan = price_query.get_plan(id)
        price = get_plan['price']
        traffic = get_plan['traffic']

        file_id = message.photo[-1].file_id
        caption = (
            f'*🛒 !خرید جدید*\n\n'
            f'💳 *روش خرید:* کارت به کارت\n'
            f'👤 *یوزرنیم:* {user_name}\n'
            f'🔋 *ترافیک پلن درخواستی:* {traffic}\n'
            f'💵 *قیمت این پلن:* {price} T'
        )
        bot.send_message(chat_id, WAITING_FOR_APPROVAL, reply_markup=admins_menu())
        markup = InlineKeyboardMarkup(row_width=2)
        button1 = InlineKeyboardButton(text='✅تایید', callback_data=f'approv_pay_{chat_id}')
        button2 = InlineKeyboardButton(text='❌رد کردن', callback_data=f'reject_pay_{chat_id}')
        markup.add(button1,button2)
        bot.send_photo(Admin_chat_id, file_id, caption=caption, parse_mode='markdown', reply_markup=markup)

        pending_payments[chat_id] = {"id": id, "user_name": user_name, "price": price, "traffic": traffic}

    else:
        bot.send_message(chat_id, "❌ لطفاً فقط عکس ارسال کنید.", reply_markup=admins_menu())
        return



@bot.callback_query_handler(func=lambda call: call.data.startswith("approv_pay_") or call.data.startswith("reject_pay_"))
def handle_payment_approval(call):
    chat_id = int(call.data.split("_")[2])

    if chat_id in pending_payments:
        data = pending_payments[chat_id]
        user_name = data['user_name']
        traffic = data['traffic']
        price = data['price']
        if call.data.startswith("approv_pay"):
            admins_query.add_traffic(user_name, traffic)
            bot.send_message(chat_id, AFTER_CONFIRM)
            caption = (
            f'✅ *پرداخت تایید شد !*\n\n'
            f'💳 *روش خرید:* کارت به کارت\n'
            f'👤 *یوزرنیم:* {user_name}\n'
            f'🔋 *ترافیک پلن درخواستی:* {traffic}\n'
            f'💵 * مبلغ پرداخت شده:* {price} T '
        )
            bot.send_message(Admin_chat_id, caption, parse_mode='markdown')
            bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            bot.send_message(chat_id, "❌ پرداخت شما رد شد. لطفاً با پشتیبانی تماس بگیرید.")
            bot.send_message(Admin_chat_id, f"❌ پرداخت {data['price']} T از {data['user_name']} رد شد.")
            bot.delete_message(call.message.chat.id, call.message.message_id)

            del pending_payments[chat_id]
    
    else:
        bot.send_message(Admin_chat_id, "❌ درخواست قدیمی است")