# type: ignore
# flake8: noqa
"""Select a New Book Page."""

import pandas as pd
import requests
import streamlit as st

from utils.database_funcs import BookDatabase

# Global Variables
BOOK_INFO: pd.DataFrame = pd.DataFrame()
BOOK_FLAG: bool = False
MORE_BOOK_INFO: dict = {}
BOOK_DATA = ()

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
get_all_books = db.get_all_books()
all_books = []

all_books = [book for book in get_all_books]


# Define data types dictionary
dtypes_dict = {
    "ISBN": str,
    "Title": str,
    "Authors": str,
    "Publisher": str,
    "Description": str,
    "Page_Count": int,
    "Year": int,
}

# Create DataFrame and apply data types
books_df = pd.DataFrame(
    # books,
    all_books,
    columns=[
        "ISBN",
        "Title",
        "Authors",
        "Publisher",
        "Description",
        "Page_Count",
        "Year",
    ],
)
books_df = books_df.astype(dtypes_dict)

only_titles = sorted(books_df["Title"].unique())

col1, col2 = st.columns([3, 5])

with col1:
    st.subheader("Select a book from the list below:")
    selected_title = st.selectbox(
        label="Select a book:",
        options=only_titles,
        index=None,
        help="The book's information will be displayed.",
        placeholder="Book title",
    )

    if selected_title:
        BOOK_INFO = books_df[selected_title == books_df["Title"]]

        # st.dataframe(BOOK_INFO)
        BOOK_FLAG = True


with col2:
    if BOOK_FLAG:
        st.subheader(f"Book Information for {BOOK_INFO['Title'].values[0]}:")
        url = f"https://covers.openlibrary.org/b/isbn/{str(BOOK_INFO['ISBN'])}-M.jpg"
        response = requests.request("GET", url)
        if response.status_code == 200:
            st.image(response.content, caption="Book Cover", use_column_width=True)
        else:
            st.error("No book cover found.")
        info1, info2 = st.columns(2)

        with st.form("add_book_form"):
            with info1:
                st.text_input(
                    "Title",
                    value=BOOK_INFO["Title"].values[0],
                    key="title",
                    disabled=True,
                )
                st.text_input(
                    "Author(s)",
                    value=BOOK_INFO["Authors"].values[0],
                    key="authors",
                    disabled=True,
                )
                st.text_input(
                    "Publisher",
                    value=BOOK_INFO["Publisher"].values[0],
                    key="publisher",
                    disabled=True,
                )
            with info2:
                st.text_input(
                    "Publication year:",
                    value=BOOK_INFO["Year"].values[0],
                    key="year",
                    disabled=True,
                )
                st.text_input(
                    "ISBN: ",
                    value=BOOK_INFO["ISBN"].values[0],
                    key="isbn",
                    disabled=True,
                )
                st.text_input(
                    "Page Count:",
                    value=BOOK_INFO["Page_Count"].values[0],
                    key="pageCount",
                    disabled=True,
                )

            add_book = st.form_submit_button(
                "Add Book", help="Add this book to your bookshelf."
            )
            if add_book:
                check_book, msg = db.check_bookshelf_entry(
                    book_id=BOOK_INFO["ISBN"].values[0], username=user_id
                )
                st.write(check_book)
                if not check_book:
                    ret_msg = db.add_to_bookshelf(
                        book_id=BOOK_INFO["ISBN"].values[0], username=user_id
                    )
                    if "success" in ret_msg:
                        st.success(f"{BOOK_INFO['Title'][0]} has been added!")
                    else:
                        st.error(f"There was an issue adding the book.\n{ret_msg}")
                else:
                    st.warning(f"Book already exists in your bookshelf.\n{msg}")

    else:
        st.subheader("Book Information:")
        st.warning("Please select a book from the list on the left.")
