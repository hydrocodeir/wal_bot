from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from config import bot, Admin_chat_id



class notif_for_main_admin:
    def start_notif(self, message):
        id = message.from_user.username
        name = message.from_user.first_name
        chat_id = message.chat.id
        caption = (
            f'🟡<b>Start notif</b>\n'
            f'<b>کاربری با مشخصات زیر ربات رو استارت کرد!</b>\n\n'
            f'👤<b>Name:</b> {name}\n'
            f'🆔<b>Username:</b> @{id} \n'
            f"<a href='tg://openmessage?user_id={chat_id}'>💬<b>Open chat</b></a>"
        )
        bot.send_message(Admin_chat_id, caption, parse_mode='HTML')

    def create_notif(self, email, admin_name, days, traffic):
        caption= (
            f'🟡<b>User creation notif</b>\n'            
            f'<b>نماینده ({admin_name}) یک کاربر ایجاد کرد !</b>\n\n'
            f'👤<b>User:</b> {email} \n'
            f'🔋<b>Traffic:</b> {traffic} \n'
            f'⌛<b>Remaining days:</b> {days} \n'
        )
        bot.send_message(Admin_chat_id, caption, parse_mode='HTML')

    def delete_notif(self, admin_name, email):
        caption = (
            f'🟡<b>Delete notif</b>\n'
            f'<b>نماینده ({admin_name}) یک کاربر رو از اینباند خودش حذف کرد!</b>\n\n'
            f'👤<b>Deleted user:</b> {email} \n'
        )
        bot.send_message(Admin_chat_id, caption, parse_mode='HTML')

    def deadline_notif(self, chat_id, username, debt_days):
        if debt_days == 3:
            caption1 = (
            f'🟡<b>Deb deadline notif</b>\n\n'
            f'<b>سه روز مهلت پرداخت برای نماینده: {username} باقی مانده!</b>')

            caption2 = (
            f'🟡<b>Deb deadline notif</b>\n\n'
            f'<b>از مهلت پرداخت صورتحساب شما فقط سه روز مانده!</b>')

            bot.send_message(
                Admin_chat_id,
                text=caption1,
                parse_mode="HTML"
                )

            bot.send_message(
                chat_id,
                text=caption2,
                parse_mode="HTML"
                )
            
        if debt_days == 0:
            caption1 = (
            f'🟡<b>Deb deadline notif</b>\n\n'
            f'<b>مهلت پرداخت بدهی برای نماینده: {username} تمام شد!</b>')

            caption2 = (
            f'🟡<b>Deb deadline notif</b>\n\n'
            f'<b>مهلت پرداخت بدهی شما به اتمام رسید!</b>')

            bot.send_message(
                Admin_chat_id,
                text=caption1,
                parse_mode="HTML"
                )

            bot.send_message(
                chat_id,
                text=caption2,
                parse_mode="HTML"
                )
            
notif_setting = notif_for_main_admin()


