import streamlit as st

st.set_page_config(
    page_title="Book Tracker",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)

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
