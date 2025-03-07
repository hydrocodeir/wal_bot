from db.query import admins_query, price_query, traffic_price_query
from keyboards.keyboards import admins_menu
from messages.messages import messages_setting
from config import bot, Admin_chat_id
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


pending_payments = {}


def receive_photo_step(message, id, chat_id):
    if message.content_type == "photo":
        get_username = admins_query.admin_data(chat_id)
        user_name = get_username["user_name"]

        get_plan = price_query.get_plan(id)
        price = get_plan["price"]
        traffic = get_plan["traffic"]

        file_id = message.photo[-1].file_id
        caption = (
            f"*🛒 !خرید جدید*\n\n"
            f"💳 *روش خرید:* کارت به کارت\n"
            f"👤 *یوزرنیم:* {user_name}\n"
            f"🔋 *ترافیک پلن درخواستی:* {traffic}\n"
            f"💵 *قیمت این پلن:* {price} T"
        )
        bot.send_message(chat_id, messages_setting.WAITING_FOR_APPROV_CARD_PAYMENT, reply_markup=admins_menu())
        markup = InlineKeyboardMarkup(row_width=2)
        button1 = InlineKeyboardButton(
            text="✅ تایید خرید", callback_data=f"approv_pay_{chat_id}"
        )
        button2 = InlineKeyboardButton(
            text="❌ رد خرید", callback_data=f"reject_pay_{chat_id}"
        )
        markup.add(button1, button2)
        bot.send_photo(
            Admin_chat_id,
            file_id,
            caption=caption,
            parse_mode="markdown",
            reply_markup=markup,
        )

        pending_payments[chat_id] = {
            "id": id,
            "user_name": user_name,
            "price": price,
            "traffic": str(traffic),
        }

    else:
        bot.send_message(
            chat_id, "❌ لطفاً فقط عکس ارسال کنید.", reply_markup=admins_menu()
        )
        return


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("approv_pay_")
    or call.data.startswith("reject_pay_")
)
def handle_payment_approval(call):
    chat_id = int(call.data.split("_")[2])

    if chat_id in pending_payments:
        data = pending_payments[chat_id]
        user_name = data["user_name"]
        traffic = data["traffic"]
        price = data["price"]
        if call.data.startswith("approv_pay"):
            admins_query.add_traffic(user_name, traffic)
            bot.send_message(chat_id, messages_setting.CONFIRM_CARD_PAYMENT)
            caption = (
                f"✅ *پرداخت تایید شد !*\n\n"
                f"💳 *روش خرید:* کارت به کارت\n"
                f"👤 *یوزرنیم نماینده:* {user_name}\n"
                f"🔋 *ترافیک درخواستی:* {traffic}\n"
                f"💵 * مبلغ پرداخت شده:* {price} T "
            )
            bot.send_message(Admin_chat_id, caption, parse_mode="markdown")
            bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            bot.send_message(
                chat_id, "❌ پرداخت شما رد شد. لطفاً با پشتیبانی تماس بگیرید."
            )
            bot.send_message(
                Admin_chat_id,
                f"❌ پرداخت {data['price']} T از {data['user_name']} رد شد.",
            )
            bot.delete_message(call.message.chat.id, call.message.message_id)

            del pending_payments[chat_id]

    else:
        bot.send_message(Admin_chat_id, "❌ درخواست قدیمی است")



pending_payments_for_debt = {}

def receive_photo_step_for_debt(message, chat_id):
    if message.content_type == "photo":
        admin_data = admins_query.admin_data(chat_id)
        user_name = admin_data["user_name"]
        price = traffic_price_query.show_price()
        debt = admin_data["debt"] * price


        file_id = message.photo[-1].file_id
        caption = (
            f"*💸 !پرداخت صورتحساب جدید*\n\n"
            f"💳 *روش پرداخت:* کارت به کارت\n"
            f"👤 *یوزرنیم نماینده:* {user_name}\n"
            f"💸 *صورتحساب نماینده:* {debt} تومان\n"
        )
        bot.send_message(chat_id, messages_setting.WAITING_FOR_APPROV_CARD_PAYMENT, reply_markup=admins_menu())
        markup = InlineKeyboardMarkup(row_width=2)
        button1 = InlineKeyboardButton(
            text="✅ تایید پرداخت", callback_data=f"_approv_pay_debt_{chat_id}"
        )
        button2 = InlineKeyboardButton(
            text="❌ رد خرید", callback_data=f"_reject_pay_debt_{chat_id}"
        )
        markup.add(button1, button2)
        bot.send_photo(
            Admin_chat_id,
            file_id,
            caption=caption,
            parse_mode="markdown",
            reply_markup=markup,
        )

        pending_payments_for_debt[chat_id] = {
            "user_name": user_name,
            "debt": debt,
        }

    else:
        bot.send_message(
            chat_id, "❌ لطفاً فقط عکس ارسال کنید.", reply_markup=admins_menu()
        )
        return



@bot.callback_query_handler(
    func=lambda call: call.data.startswith("_approv_pay_debt_")
    or call.data.startswith("_reject_pay_debt_")
)

def handle_debt_payment_approval(call):
    chat_id = int(call.data.split("_")[4])

    if chat_id in pending_payments_for_debt:
        data = pending_payments_for_debt[chat_id]
        user_name = data["user_name"]
        debt = data["debt"]

        if call.data.startswith("_approv_pay_debt"):
            new_dead_line = traffic_price_query.show_dead_line()
            admins_query.clear_debt(chat_id, new_dead_line)
            bot.send_message(chat_id, messages_setting.CONFIRM_CARD_PAYMENT)

            caption = (
                f"✅ *پرداخت تایید شد!*\n\n"
                f"💳 *روش پرداخت:* کارت به کارت\n"
                f"👤 *یوزرنیم نماینده:* {user_name}\n"
                f"💸 *بدهی پرداخت شده:* {debt} تومان"
            )
            bot.send_message(Admin_chat_id, caption, parse_mode="markdown")
            bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            bot.send_message(chat_id, "❌ پرداخت شما رد شد. لطفاً با پشتیبانی تماس بگیرید.")
            bot.send_message(Admin_chat_id, f"❌ پرداخت از {user_name} رد شد.")
            bot.delete_message(call.message.chat.id, call.message.message_id)

        del pending_payments_for_debt[chat_id]

    else:
        bot.send_message(Admin_chat_id, "❌ درخواست قدیمی است.")
