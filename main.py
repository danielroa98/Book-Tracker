import streamlit as st
from utils.auth import Authenticator

st.set_page_config(
    page_title="Book Tracker",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Instantiate Auth class
auth = Authenticator()

# Initialize session state for login status
auth.init_session()

# Login or register forms
if not auth.is_logged_in():
    st.title("Book Tracker 📚")

    # Registration form
    if st.session_state.get("register", False):
        st.header("Register")
        reg_username = st.text_input("Username")
        reg_password = st.text_input("Password", type="password")
        if st.button("Register"):
            if reg_username and reg_password:
                auth.register_user(reg_username, reg_password)
                st.success("Registration successful. Please log in.")
                st.session_state["register"] = False
            else:
                st.error("Please enter a username and password.")
        if st.button("Go to Login"):
            st.session_state["register"] = False
    else:
        # Login form
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if auth.login(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Invalid username or password")
        if st.button("Go to Register"):
            st.session_state["register"] = True
else:
    st.title("Book Tracker 📚")
    st.write(
        """
        Welcome to the Book Tracker app! This application allows you to scan book barcodes, retrieve book information, and add books to your personal database.

        ### Navigation
        - **New Book**: Add a new book to your database by scanning its barcode or uploading an image of the barcode.
        - **View Books**: Displays all of the books you've registered to your own database.
        - **Select Book**: Allows you to edit a book's values, in particular the page you are currently at.
        """
    )
    if st.button("Logout"):
        auth.logout()
        st.rerun()
