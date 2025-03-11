from config import bot
import time
import os
import sqlite3


DB_PATH = "data/wal.db"
TEMP_DB_PATH = "data/wal_new.db"

def send_backup(message):
    with open(DB_PATH, "rb") as db_file:
        bot.send_message(
            message.chat.id,
            "درحال دریافت بکاپ..."
            )
        time.sleep(2)

        bot.send_document(
            message.chat.id,
            db_file,
            caption=f"{time.strftime('%Y-%m-%d  --  %H:%M', time.localtime())}"
            )
    

def restore_backup(message):
    if not message.document:
        bot.send_message(message.chat.id, "❌ لطفاً فقط فایل `wal.db` ارسال کنید.")
        return
    else:
        print("OK")
        file_info = bot.get_file(message.document.file_id)
        if message.document.file_name == "wal.db":
            file_path = file_info.file_path
            download_file = bot.download_file(file_path)

            with open(TEMP_DB_PATH, "wb") as new_db:
                new_db.write(download_file)

            os.replace(TEMP_DB_PATH, DB_PATH)

            bot.send_message(
                message.chat.id,
                "✅ دیتابیس با موفقیت جایگزین شد."
            )
            # os._exit(1)
        else:
            bot.send_message(
                message.chat.id,
                "❌ لطفاً فقط فایل `wal.db` ارسال کنید.")
