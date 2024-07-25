import streamlit as st
import pandas as pd
import time
from datetime import datetime
from utils.database_funcs import BookDatabase

st.set_page_config(
    page_title="Select a Book",
    page_icon="📕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("View a Book 📕")

db = BookDatabase("books.db")
books = db.get_all_books()

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
    books,
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
                            disabled=False,
                        )
                        authors = st.text_input(
                            label="Book's author(s)",
                            value=book_info[2],
                            key="authors",
                            help="The author(s) of the book.",
                            disabled=False,
                        )
                        publisher = st.text_input(
                            label="Publisher",
                            value=book_info[3],
                            key="publisher",
                            help="The publisher of the book.",
                            disabled=False,
                        )
                        year = st.text_input(
                            label="Year of Publication",
                            value=book_info[6],
                            key="year",
                            help="The year the book was published.",
                            disabled=False,
                        )

                    with book2:
                        description = st.text_area(
                            label="Description",
                            value=book_info[4],
                            key="description",
                            help="A brief description of the book.",
                            disabled=False,
                        )
                        page_count = st.number_input(
                            label="Page Count",
                            value=book_info[5],
                            key="page_count",
                            help="The number of pages in the book.",
                            disabled=False,
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
                            options=["Yes", "No"],
                            index=1,
                            key="owned",
                            help="Indicates whether you own the book.",
                            disabled=False,
                        )

                    submitted = st.form_submit_button(
                        "Update Book Info",
                        help="Update the book's information in the database.",
                    )

if selected_title:
    if submitted:
        update_msg = db.update_book(
            isbn=book_info[0],
            title=title,
            authors=authors,
            publisher=publisher,
            description=description,
            page_count=page_count,
            year=year,
            started_reading=str(started_reading) if started_reading else None,
            ended_reading=str(finished_reading) if finished_reading else None,
            owned=owned,
            current_page=current_page,
        )
        if "successfully" in update_msg:
            st.success(update_msg)
        else:
            st.error(update_msg)
        with st.container(border=True):
            st.markdown(
                f"""
                        Book's new information is:\n
                        {title}\n
                        {authors}\n
                        {publisher}\n
                        {description}\n
                        {page_count}\n
                        {year}\n
                        {started_reading}\n
                        {finished_reading}\n
                        {owned}\n
                        {current_page}\n
                        """
            )
