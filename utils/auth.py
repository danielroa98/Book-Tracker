""""Authentication utilities for user registration, login, and logout."""

import bcrypt
import sqlite3
import streamlit as st
import os

from pydantic.dataclasses import dataclass

@dataclass
class Authenticator:

    db_name: str = os.path.join(os.path.dirname(__file__), "..", "users.db")

    def __post_init__(self):
        self.validate_db_existance()
    
    def validate_db_existance(self):
        if not os.path.exists(self.db_name):
            self.init_db(self.db_name)

    def init_db(self, db_name: str) -> str:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("""CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)""")
            conn.commit()
            return "Database initialized."
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()
    
    # Hashing and checking passwords
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    def check_password(self, hashed_password, plain_password):
        return bcrypt.checkpw(plain_password.encode(), hashed_password)

    # User registration    
    def register_user(self, username, password):
        hashed_pw = self.hash_password(password)
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            conn.commit()
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()
        
    # User login
    def login(self, username, password):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = c.fetchone()
            if result and self.check_password(result[0], password):
                return True
            return False
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()
        
    # User logout
    def logout(self):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
    
    def is_logged_in(self):
        return st.session_state.get("logged_in", False)

    # Initialize session
    def init_session(self):
        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = False
