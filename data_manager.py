 
import sqlite3
import uuid
 
conn = sqlite3.connect("pastes_clone.db", check_same_thread=False)
 
cursor = conn.cursor()
 
# cursor.execute("Drop table pastes_clone")
 
cursor.execute("""CREATE TABLE IF NOT EXISTS pastes_clone
               (
               paste_id STRING PRIMARY KEY,
               title TEXT NOT NULL,
               content TEXT NOT NULL,
               expiry STRING ,
               is_password_protected STRING DEFAULT 0,
               password STRING,
               language STRING,
               burn_after_read  
               )""")

def add_entry(uid, title,content, expiry, is_password, password, language, burn_after_read):
    
    cursor.execute(f"""
                   INSERT INTO pastes_clone (paste_id, title,content, expiry, is_password_protected, password, language, burn_after_read) VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?)
                   """,
                   (uid,title,content, expiry, is_password, password,language, burn_after_read))
 
    conn.commit()

def get_data(id):

    cursor.execute(f"SELECT * FROM pastes_clone WHERE paste_id ='{id}'")

    results = cursor.fetchall()

    return results

def delete_entry(uid):
    cursor.execute(f"DELETE FROM pastes_clone WHERE paste_id = '{uid}' ")
    conn.commit()

 
conn.commit()
# conn.close()