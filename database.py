import sqlite3

def get_connection():
    return sqlite3.connect("security.db", check_same_thread=False)

    def create_tables():
        conn = get_connection()
            cur = conn.cursor()

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                            username TEXT PRIMARY KEY,
                                    password_hash TEXT,
                                            locked INTEGER DEFAULT 0
                                                )
                                                    """)

                                                        cur.execute("""
                                                            CREATE TABLE IF NOT EXISTS login_attempts (
                                                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                            username TEXT,
                                                                                    success INTEGER,
                                                                                            timestamp TEXT
                                                                                                )
                                                                                                    """)

                                                                                                        conn.commit()
                                                                                                            conn.close()
                                                                                                            
