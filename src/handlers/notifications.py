from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from config import bot, Admin_chat_id



class notif_for_main_admin:
    def start_notif(self, message):
        id = message.from_user.username
        name = message.from_user.first_name
        caption = (
            f'🟡*Start notif*\n'
            f'*کاربری با مشخصات زیر ربات رو استارت کرد!*\n\n'
            f'👤*name:* {name}\n'
            f'🆔*username:* @{id} \n'
        )
        bot.send_message(Admin_chat_id, caption, parse_mode='markdown')



    def delete_notif(self, admin_name, email):
        caption = (
            f'🟡*Delete notif*\n'
            f'*نماینده ({admin_name}) یک کاربر رو از اینباند خودش حذف کرد!*\n\n'
            f'🗑️*user:* {email} \n'
        )
        bot.send_message(Admin_chat_id, caption, parse_mode='markdown')

notif_setting = notif_for_main_admin()


