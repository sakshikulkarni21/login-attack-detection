import streamlit as st
from database import create_tables, get_connection
from auth import hash_password, verify_password
from attack_detection import check_bruteforce
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Login Attack Detection", page_icon="🔐")

create_tables()

st.title("🔐 Login Attack Detection Simulator")

conn = get_connection()
cur = conn.cursor()

# Create demo user
cur.execute("SELECT * FROM users WHERE username = 'admin'")
if cur.fetchone() is None:
    cur.execute(
        "INSERT INTO users VALUES (?, ?, ?)",
        ("admin", hash_password("Admin@123"), 0)
    )
    conn.commit()

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    cur.execute(
        "SELECT password_hash, locked FROM users WHERE username = ?",
        (username,)
    )
    user = cur.fetchone()

    if user is None:
        st.error("User not found")

    else:
        password_hash, locked = user

        if locked:
            st.error("Account locked due to suspicious activity")

        else:
            if verify_password(password, password_hash):
                st.success("Login successful")
                cur.execute(
                    "INSERT INTO login_attempts (username, success, timestamp) VALUES (?, ?, ?)",
                    (username, 1, datetime.now().isoformat())
                )

            else:
                st.error("Invalid password")
                cur.execute(
                    "INSERT INTO login_attempts (username, success, timestamp) VALUES (?, ?, ?)",
                    (username, 0, datetime.now().isoformat())
                )

                if check_bruteforce(username):
                    cur.execute(
                        "UPDATE users SET locked = 1 WHERE username = ?",
                        (username,)
                    )
                    st.warning("Account locked due to brute-force attempts")

            conn.commit()

st.subheader("📊 Login Attempts Dashboard")

df = pd.read_sql("SELECT * FROM login_attempts", conn)
st.dataframe(df)
