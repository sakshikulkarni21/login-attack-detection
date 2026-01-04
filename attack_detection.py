import sqlite3

THRESHOLD = 5

def check_bruteforce(username):
    conn = sqlite3.connect("security.db")
        cur = conn.cursor()

            cur.execute("""
                SELECT COUNT(*) FROM login_attempts
                    WHERE username = ? AND success = 0
                        """, (username,))

                            failed_attempts = cur.fetchone()[0]
                                conn.close()

                                    return failed_attempts >= THRESHOLD
                                    
