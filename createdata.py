import sqlite3

conn = sqlite3.Connection('wal.db')
cursor = conn.cursor()


# selers id
cursor.execute('''
CREATE TABLE IF NOT EXISTS sellers (
    id INTEGER PRIMARY KEY,
    inb_id INTEGER
)
''')

conn.commit()
conn.close()




# add seller
def add_seller(seller_id, inb_id):
    conn = sqlite3.connect('wal.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO sellers (id, inb_id) VALUES (?, ?)',
            (seller_id, inb_id)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:

        return False
    finally:
        conn.close()



# del seller
def delete_seller(seller_id):
    with sqlite3.connect('wal.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sellers WHERE id = ?', (seller_id,))
        conn.commit()



#show seller
def get_all_sellers():
    with sqlite3.connect('wal.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM sellers')
        sellers = [row[0] for row in cursor.fetchall()]
    return sellers


def is_seller(chat_id):
    conn = sqlite3.connect('wal.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM sellers WHERE id = ?', (chat_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result is not None 


# get id for create user
def get_inb_id(chat_id):
    conn = sqlite3.connect('wal.db')
    cursor = conn.cursor()
    cursor.execute("SELECT inb_id FROM sellers WHERE id = ?", (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


