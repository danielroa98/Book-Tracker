# type: ignore
"""Select a New Book Page."""

import pandas as pd
import streamlit as st

from utils.database_funcs import BookDatabase

# Global Variables
BOOK_INFO: dict = {}
MORE_BOOK_INFO: dict = {}

st.set_page_config(
    page_title="Add a new book",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Retrieve the user ID from the session state
user_id = st.session_state.get("username", None)

if user_id is None:
    st.error("You must be logged in to add a book.")
    st.stop()  # Stop the script here if the user is not logged in

st.title("Add a new book 📖")

db = BookDatabase("books.db", "bookshelf.db")
all_books = db.get_all_books()[0]
st.write(all_books)

# Define data types dictionary
dtypes_dict = {
    "ISBN": str,
    "Title": str,
    "Authors": str,
    "Publisher": str,
    "Description": str,
    "Page_Count": int,
    "Year": int,
    "Started_Reading": "datetime64[ns]",
    "Finished_Reading": "datetime64[ns]",
    "Owned": "category",
    "Current_Page": int,
}

# Create DataFrame and apply data types
books_df = pd.DataFrame(
    # books,
    [all_books],
    columns=[
        "ISBN",
        "Title",
        "Authors",
        "Publisher",
        "Description",
        "Page_Count",
        "Year",
        "Started_Reading",
        "Finished_Reading",
        "Owned",
        "Current_Page",
    ],
)
books_df = books_df.astype(dtypes_dict)

st.dataframe(books_df)

only_titles = sorted(books_df["Title"].unique())

col1, col2 = st.columns([4, 3])

with col1:
    st.subheader("Select a book from the list below:")
    selected_title = st.selectbox(
        label="Select a book:",
        options=only_titles,
        index=None,
        help="The book's information will be displayed.",
        placeholder="Book title",
    )

    book_info = db.get_book_by_title(selected_title)
