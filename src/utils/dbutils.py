import sqlite3
import bcrypt
from typing import List, Tuple, Optional, Dict
import uuid
from datetime import datetime
import os
DB_PATH = os.environ.get("DB_PATH", "users.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            full_name TEXT,
            email TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Chat history table with chat_name
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            chat_id TEXT NOT NULL,
            chat_name TEXT,
            role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username)
        );
    """)

    conn.commit()
    conn.close()

def create_user(username: str, full_name: str, email: str, password: str) -> bool:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        cursor.execute("""
            INSERT INTO users (username, full_name, email, password_hash)
            VALUES (?, ?, ?, ?)
        """, (username, full_name, email, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_username(username: str) -> Optional[Dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "username": row[1],
            "full_name": row[2],
            "email": row[3],
            "password_hash": row[4],
            "created_at": row[5]
        }
    return None

def verify_user_credentials(username: str, password: str) -> bool:
    user = get_user_by_username(username)
    if user:
        return bcrypt.checkpw(password.encode(), user["password_hash"].encode())
    return False

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, full_name, email, created_at FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_user(username: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def update_user_password(username: str, new_password: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (new_hash, username))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated

def insert_message(username: str, chat_id: str, role: str, message: str) -> bool:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_history (username, chat_id, role, message)
            VALUES (?, ?, ?, ?)
        """, (username, chat_id, role, message))
        conn.commit()
        return True
    except Exception as e:
        print("Error inserting message:", e)
        return False
    finally:
        conn.close()

def get_chat_history(chat_id: str, n: int = 3) -> List[Tuple[str, str]]:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT role, message FROM chat_history
            WHERE chat_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (chat_id, n))
        rows = cursor.fetchall()
        return rows[::-1]
    except Exception as e:
        print("Error retrieving chat history:", e)
        return []
    finally:
        conn.close()

def delete_chat_history(chat_id: Optional[str] = None, username: Optional[str] = None) -> int:
    if not chat_id and not username:
        raise ValueError("Either chat_id or username must be provided.")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        if chat_id:
            cursor.execute("DELETE FROM chat_history WHERE chat_id = ?", (chat_id,))
        elif username:
            cursor.execute("DELETE FROM chat_history WHERE username = ?", (username,))
        deleted_rows = cursor.rowcount
        conn.commit()
        return deleted_rows
    except Exception as e:
        print("Error deleting chat history:", e)
        return 0
    finally:
        conn.close()

def generate_chat_id(username: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"{username}_{timestamp}_{uuid.uuid4().hex[:8]}"

def get_all_chat_ids_for_user(username: str) -> List[Tuple[str, Optional[str]]]:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT chat_id, chat_name
            FROM chat_history
            WHERE username = ?
            GROUP BY chat_id
            ORDER BY MAX(timestamp) DESC
        """, (username,))
        return cursor.fetchall()
    except Exception as e:
        print("Error retrieving chat IDs:", e)
        return []
    finally:
        conn.close()

def update_chat_name(chat_id: str, new_name: str) -> bool:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE chat_history SET chat_name = ? WHERE chat_id = ?", (new_name, chat_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("Error updating chat name:", e)
        return False
    finally:
        conn.close()

def migrate_add_chat_name_column():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(chat_history);")
        columns = [col[1] for col in cursor.fetchall()]
        if "chat_name" not in columns:
            cursor.execute("ALTER TABLE chat_history ADD COLUMN chat_name TEXT;")
            conn.commit()
            print("✅ 'chat_name' column added.")
    except Exception as e:
        print("Migration error:", e)
    finally:
        conn.close()

def delete_chat(chat_id: str) -> bool:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_history WHERE chat_id = ?", (chat_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("Error deleting chat:", e)
        return False
    finally:
        conn.close()