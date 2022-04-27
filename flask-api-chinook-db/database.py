import sqlite3

def run_query(sql, params = ()):

    #grab data from DB
    db = sqlite3.connect('chinook.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def run_total(sq1, params = ()):
    db = sqlite3.connect('chinook.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(sq1, params)
    result = cursor.fetchone() [0]
    cursor.close()
    db.close()
    return id

def run_insert(sql, params):
    #grab data from DB
    db = sqlite3.connect('chinook.db')
    cursor = db.cursor()
    cursor.execute(sql, params)
    result = cursor.lastrowid
    db.commit()
    cursor.close()
    db.close()
    return result

def run_delete_cart(sq1, params):
    db = sqlite3.connect('chinook.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(sq1, params)
    result = cursor.lastrowid
    db.commit()
    cursor.close()
    db.close()
    return result

def run_remove_cart(sq1, params):
    db = sqlite3.connect('chinook.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(sq1, params)
    result = cursor.lastrowid
    db.commit()
    cursor.close()
    db.close()
    return result

def run_clear_cart(sq1, params):
    db = sqlite3.connect('chinook.db')
    db.row_factory = sqlite3.Row
    crusor = db.cursor()
    cursor.execute(sq1)
    result = cursor.lastrowid
    db.commit()
    cursor.close()
    db.close()
    return result
