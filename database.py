import sqlite3

from config import DB_NAME

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users(
             user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
             name TEXT, 
             number TEXT
             )''')
conn.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS products(
             id INTEGER PRIMARY KEY AUTOINCREMENT, 
             product_name TEXT NOT NULL UNIQUE
             )''')
conn.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS answers(
             id INTEGER PRIMARY KEY AUTOINCREMENT, 
             title TEXT,
             description TEXT,
             video TEXT,
             product_id INTEGER,
             FOREIGN KEY(product_id) REFERENCES products(id)
             )''')
conn.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS questions(
             id INTEGER PRIMARY KEY AUTOINCREMENT, 
             title TEXT,
             description TEXT,
             video TEXT,
             user_id INTEGER,
             product_id INTEGER,
             status TEXT,
             FOREIGN KEY(user_id) REFERENCES users(user_id),
             FOREIGN KEY(product_id) REFERENCES products(id)
             )''')
conn.commit()

l = ["Aniterror", "Interaktiv universal o`q otish tiri", "Desant tayyorlash trenajyori",
     "O`q otish trenajyori(zarb tasir kuchi bilan)", "Panaramali tir", "BTR 80 trenajyori", "PZRK",
     "Avtomabil boshqaruv simulatori(UAZ Hunter)", "Elektron kutubxona", "Multimediali tir",
     "Nishonlarni ko`tarish(turish) uchun masofadan-boshqariladigan moslamalar vzvod to`plami"]
for i in l:
    try:
        cursor.execute(f"INSERT INTO products (product_name) VALUES ('{i}')")
        conn.commit()
    except:
        pass
