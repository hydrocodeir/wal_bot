import sqlite3
import os


db_path = os.path.join(os.path.dirname(__file__), 'wal.db')
conn = sqlite3.Connection(db_path)
cursor = conn.cursor()


# admins table
cursor.execute('''
CREATE TABLE IF NOT EXISTS admins (
    chat_id INTEGER,
    user_name TEXT PRIMARY KEY,
    password TEXT,
    traffic INTEGER,
    inb_id INTEGER
)
''')

conn.commit()
conn.close()



# add admin
def add_admin(user_name, password, traffic, inb_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO admins (user_name, password, traffic, inb_id) VALUES (?, ?, ?, ?)',
            (user_name, password, traffic, inb_id)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:

        return False
    finally:
        conn.close()


#change inb id
def change_inb_id(user_name, new_inb):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE LOWER(user_name) = LOWER(?)", (user_name,))
        admin = cursor.fetchone()
        
        if admin:
            cursor.execute("UPDATE admins SET inb_id = ? WHERE user_name = ?", (new_inb, user_name))
            conn.commit()
            return True
        else:
            return False


# add trafic
def add_traffic_for_admin(user_name, traffic):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE LOWER(user_name) = LOWER(?)", (user_name,))
        admin = cursor.fetchone()

        if admin:
            cursor.execute(
                "UPDATE admins SET traffic = traffic + ? WHERE user_name = ?",
                (traffic, user_name)
            )
            conn.commit()
            return True
        else:
            return False


# del admin
def delete_admin(user_name):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM admins WHERE user_name = ?', (user_name,))
        conn.commit()

    if logged_in_users:
        for chat_id, data in logged_in_users.items():
            if data['user_name'] == user_name:
                del logged_in_users[chat_id]
                break



#show admins
def get_all_admins():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_name, traffic, inb_id FROM admins')
        admins = [
            {"user_name": row[0], "traffic": row[1], "inb_id": row[2]} 
            for row in cursor.fetchall()
        ]
    return admins



# login/logout system
logged_in_users = {}

def login_user(user_name, password, chat_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE user_name = ? AND password = ?", (user_name, password))
        user = cursor.fetchone()
        
        if user:
            logged_in_users[chat_id] = {
                'user_name': user_name,
                'password': password,
                'traffic': user[3],
                'inb_id': user[4] 
            }
            return True
        else:
            return False
        
def save_admin_login(chat_id, user_name):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE admins
                SET chat_id = ?
                WHERE user_name = ?
            """, (chat_id, user_name))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error in save_admin_login: {e}")


def logout_user(chat_id):
    if chat_id in logged_in_users:
        del logged_in_users[chat_id]
        return True
    else:
        return False

def check_if_logged_in(chat_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM admins WHERE chat_id = ?", (chat_id,))
        result = cursor.fetchone()
        return result[0] > 0


# get id for create user
def get_inb_id(chat_id):
    if chat_id in logged_in_users:
        return logged_in_users[chat_id]['inb_id']
    else:
        return None
    
# get admin traffic
def get_admin_traffic(chat_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT traffic FROM admins WHERE chat_id = ?', (chat_id,))
        result = cursor.fetchone()
        return float(result[0]) if result else None

def update_admin_traffic(chat_id, delta):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT traffic FROM admins WHERE chat_id = ?', (chat_id,))
            result = cursor.fetchone()
            
            if result is None:
                return False
            
            current_traffic = float(result[0])
            new_traffic = current_traffic + delta
            
            if new_traffic < 0:
                new_traffic = 0
            
            cursor.execute('UPDATE admins SET traffic = ? WHERE chat_id = ?', (new_traffic, chat_id))
            conn.commit()
            return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False



# Change help message
def change_help_message(filename, var_name, new_text):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(filename, "w", encoding="utf-8") as file:
        for line in lines:
            if line.startswith(var_name):
                file.write(f'{var_name} = """{new_text}"""\n')
            else:
                file.write(line)
