import pandas as pd
import sqlite3 as db

def get_history():
    db_file = 'chat_db.db'
    conn = db.connect(db_file)
    df = pd.read_sql_query("SELECT * from chat_history", conn)
    conn.close()
    return df

def insert_db(session,role,content):
    db_file = 'chat_db.db'
    conn = db.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(f'''insert into chat_history (session_name,chat_id,role,content) 
               values 
               ('{session}',
                COALESCE((select max(chat_id) from chat_history 
                          where session_name="{session}"),0)+1 ,
                '{role}',
               '{content.replace("'","''")}')
               ''')
    conn.commit()

    conn.close()

def delete_db(session):
    db_file = 'chat_db.db'
    conn = db.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(f'''delete from chat_history 
               where session_name = "{session}"
               ''')
    conn.commit()

    conn.close()
