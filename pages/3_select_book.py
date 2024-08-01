# type: ignore
"""Select Book."""

from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from utils.database_funcs import BookDatabase

st.set_page_config(
    page_title="Select a Book",
    page_icon="📕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Retrieve the user ID from the session state
user_id = st.session_state.get("username", None)

if user_id is None:
    st.error("You must be logged in to add a book.")
    st.stop()  # Stop the script here if the user is not logged in


db = BookDatabase("books.db", "bookshelf.db")
all_user_books = db.get_from_bookshelf(username=user_id)  # type: ignore

user_books = [book for book in all_user_books]

if all_user_books:

    st.title("View a Book 📕")
    # st.markdown(user_books)

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
        user_books,
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

    only_titles = sorted(books_df["Title"].unique())

    col1, col2 = st.columns([1, 4], gap="small")

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

    with col2:
        if selected_title:
            st.subheader(f"{selected_title} 📕")
            if selected_title and book_info:
                with st.container():
                    book1, book2, book3 = st.columns([2, 4, 2])

                    with st.form(key="book_info", border=False):
                        with book1:
                            title = st.text_input(
                                label="Book's title",
                                value=book_info[1],
                                key="title",
                                help="The title of the book.",
                                disabled=True,
                            )
                            authors = st.text_input(
                                label="Book's author(s)",
                                value=book_info[2],
                                key="authors",
                                help="The author(s) of the book.",
                                disabled=True,
                            )
                            publisher = st.text_input(
                                label="Publisher",
                                value=book_info[3],
                                key="publisher",
                                help="The publisher of the book.",
                                disabled=True,
                            )
                            year = st.text_input(
                                label="Year of Publication",
                                value=book_info[6],
                                key="year",
                                help="The year the book was published.",
                                disabled=True,
                            )

                        with book2:
                            description = st.text_area(
                                label="Description",
                                value=book_info[4],
                                key="description",
                                help="A brief description of the book.",
                                disabled=True,
                            )
                            page_count = st.number_input(
                                label="Page Count",
                                value=book_info[5],
                                key="page_count",
                                help="The number of pages in the book.",
                                disabled=True,
                                min_value=0,
                                step=1,
                                format="%d",
                            )
                            current_page = st.number_input(
                                label="Current Page",
                                value=book_info[10],
                                key="current_page",
                                help="The current page you are on.",
                                disabled=False,
                                min_value=0,
                                max_value=page_count,
                                step=1,
                                format="%d",
                            )

                        with book3:
                            started_reading = st.date_input(
                                label="Date Started Reading",
                                value=pd.to_datetime(book_info[7], errors="coerce"),
                                key="started_reading",
                                help="The date the book was started.",
                                format="DD/MM/YYYY",
                                max_value=datetime.now(),
                            )
                            if current_page < page_count:
                                st.info("You haven't finished your book.")
                                finished_reading = (
                                    started_reading + timedelta(days=365)
                                ).strftime("%Y-%m-%d")
                            else:
                                finished_reading = st.date_input(
                                    label="Date Finished Reading",
                                    value=pd.to_datetime(book_info[8], errors="coerce"),
                                    key="finished_reading",
                                    help="The date the book was finished.",
                                    format="DD/MM/YYYY",
                                    max_value=datetime.now(),
                                )
                            owned = st.selectbox(
                                label="Owned",
                                options=["Owned", "Rented", "Burrowed", "No"],
                                index=None,
                                key="owned",
                                help="Indicates whether you own the book.",
                                disabled=True,
                                placeholder="Own",
                            )

                        opt1, opt2 = st.columns(2)
                        with opt1:
                            updated_book = st.form_submit_button(
                                "Update Book Info",
                                help="Update the book's info.",
                                type="primary",
                            )

                        with opt2:
                            delete_book = st.form_submit_button(
                                "Delete Book",
                                help="Delete the book from your bookshelf.",
                                type="secondary",
                            )

    if selected_title:
        col1, col2 = st.columns(2)
        if updated_book:
            possible, update_msg = db.update_bookshelf(
                book_id=book_info[0],
                username=user_id,
                date_started=started_reading,
                date_ended=finished_reading,
                owned="Own",
                current_page=current_page,
            )
            if "successfully" in update_msg:
                with col1:
                    st.success(update_msg)
            else:
                with col1:
                    st.error(update_msg)
        elif delete_book:
            delete_msg = db.remove_from_bookshelf(
                book_id=book_info[0], username=user_id
            )
            if "removed" in delete_msg:
                with col2:
                    st.success(delete_msg)
                    st.rerun()
            else:
                with col2:
                    st.error(delete_msg)
            # if owned == "No":
            #     rem_ans = db.remove_from_bookshelf(book_info[0], user_id)
            #     if "removed" in rem_ans:
            #         with col2:
            #             st.success(rem_ans)
            #     else:
            #         with col2:
            #             st.error(rem_ans)
            # elif owned == "Owned":
            #     add_ans = db.add_to_bookshelf(book_info[0], user_id)
            #     if "added" in add_ans:
            #         with col2:
            #             st.success(add_ans)
            #     else:
            #         with col2:
            #             st.error(add_ans)

else:
    st.header("You have not added any books yet.")
