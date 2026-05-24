import sqlite3
import json

DB_NAME = "chat_history.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chats (
            chat_name TEXT PRIMARY KEY,
            messages TEXT
        )
        """
    )

    conn.commit()

    conn.close()


def save_chat(chat_name, messages):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    messages_json = json.dumps(messages)

    cursor.execute(
        """
        INSERT OR REPLACE INTO chats
        (chat_name, messages)
        VALUES (?, ?)
        """,
        (chat_name, messages_json)
    )

    conn.commit()

    conn.close()


def load_all_chats():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT chat_name, messages FROM chats"
    )

    rows = cursor.fetchall()

    conn.close()

    chats = {}

    for row in rows:

        chats[row[0]] = json.loads(row[1])

    return chats


def delete_all_chats():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM chats")

    conn.commit()

    conn.close()

def delete_chat(chat_name):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM chats WHERE chat_name = ?",
        (chat_name,)
    )

    conn.commit()

    conn.close()