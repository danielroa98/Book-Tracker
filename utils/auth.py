# flake8: noqa
""""Authentication utilities for user registration, login, and logout."""

import os
import sqlite3

import bcrypt
import streamlit as st
from pydantic.dataclasses import dataclass


@dataclass
class Authenticator:
    """
    The Authenticator class provides methods for user authentication and session management.

    Attributes:
        db_name (str): The path to the database file.

    Methods:
        __post_init__(): Initializes the Authenticator object and validates the existence of the database.
        validate_db_existance(): Checks if the database file exists and initializes it if not.
        init_db(db_name: str) -> str: Initializes the database by creating the 'users' table.
        hash_password(password): Hashes a password using bcrypt.
        check_password(hashed_password, plain_password): Checks if a plain password matches a hashed password.
        register_user(username, password): Registers a new user by inserting their username and hashed password into the database.
        login(username, password): Authenticates a user by checking their username and password against the database.
        logout(): Logs out the current user by resetting the session state.
        is_logged_in(): Checks if a user is currently logged in.
        init_session(): Initializes the session by setting the initial session state.
    """

    db_name: str = os.path.join(os.path.dirname(__file__), "..", "users.db")

    def __post_init__(self) -> None:
        """
        Performs post-initialization tasks for the class instance.

        This method is automatically called after the instance has been initialized.
        It is used to perform any additional setup or validation required for the instance.

        Returns:
            None
        """
        self.validate_db_existance()

    def validate_db_existance(self) -> None:
        """
        Checks if the database file exists. If not, initializes a new database.

        Returns:
            None
        """
        if not os.path.exists(self.db_name):
            self.init_db(self.db_name)

    def init_db(self, db_name: str) -> str:
        """
        Initializes the database by creating the 'users' table if it doesn't exist.

        Args:
            db_name (str): The name of the database.

        Returns:
            str: A message indicating whether the database was successfully initialized or if an error occurred.
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute(
                """CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)"""
            )
            conn.commit()
            return "Database initialized."
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()

    # Hashing and checking passwords
    def hash_password(self, password: str) -> bcrypt.hashpw:  # type: ignore
        """
        Hashes the given password using bcrypt.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def check_password(self, hashed_password: bcrypt.hashpw, plain_password: str) -> bcrypt.checkpw:  # type: ignore
        """
        Check if a plain password matches a hashed password.

        Parameters:
        - hashed_password (str): The hashed password to compare.
        - plain_password (str): The plain password to compare.

        Returns:
        - bool: True if the plain password matches the hashed password, False otherwise.
        """
        return bcrypt.checkpw(plain_password.encode(), hashed_password)

    # User registration
    def register_user(self, username: str, password: str) -> str:
        """
        Registers a new user in the database.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            str: A success message if the user is registered successfully,
                 or an error message if an exception occurs during the registration process.
        """
        hashed_pw = self.hash_password(password)
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_pw),
            )
            conn.commit()
            return "User registered successfully."
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()

    # User login
    def login(self, username: str, password: str) -> bool | str:
        """
        Authenticates a user by checking their username and password against the database.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the authentication is successful, False otherwise.
            str: An error message if an exception occurs during the authentication process.
        """
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
    def logout(self) -> None:
        """Logs out the user by setting the 'logged_in' flag to False and clearing the 'username' session state."""
        st.session_state["logged_in"] = False
        st.session_state["username"] = None

    def is_logged_in(self) -> st.session_state:  # type: ignore
        """
        Check if the user is logged in.

        Returns:
            bool: True if the user is logged in, False otherwise.
        """
        return st.session_state.get("logged_in", False)

    # Initialize session
    def init_session(self) -> None:
        """
        Initializes the session by checking if the user is logged in.

        If the 'logged_in' key is not present in the session state, it sets it to False.

        Parameters:
            None

        Returns:
            None
        """
        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = False
