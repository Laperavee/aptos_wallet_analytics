import sqlite3

def init_db():
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS wallets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  address TEXT UNIQUE, 
                  user_id TEXT)''')
    conn.commit()
    conn.close()

def add_wallet(address, user_id):
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO wallets (address, user_id) VALUES (?, ?)", (address, user_id))
        conn.commit()
    except sqlite3.IntegrityError:
        return f"L'adresse {address} est déjà surveillée."
    conn.close()
    return f"L'adresse {address} a été ajoutée."

def remove_wallet(address):
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()
    c.execute("DELETE FROM wallets WHERE address=?", (address,))
    conn.commit()
    conn.close()
    return f"L'adresse {address} a été supprimée."

def get_wallets():
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()
    c.execute("SELECT address, user_id FROM wallets")  # Récupérer l'ID de l'utilisateur également
    wallets = c.fetchall()
    conn.close()
    return [{'address': wallet[0], 'user_id': wallet[1]} for wallet in wallets]  # Formatage en dictionnaire
