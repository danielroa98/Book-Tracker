import time
from datetime import datetime

import pandas as pd
import streamlit as st

from utils.database_funcs import BookDatabase

st.set_page_config(
    page_title="View All Books",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("View All Books 📚")

db = BookDatabase("books.db")
books = db.get_all_books()

# Define data types dictionary
dtypes_dict = {
    "ISBN": str,
    "Title": str,
    "Authors": str,
    "Publisher": str,
    "Description": str,
    "Page Count": int,
    "Year": int,
    "Started Reading": "datetime64[ns]",
    "Finished Reading": "datetime64[ns]",
    "Owned": "category",
    "Current Page": int,
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
        "Page Count",
        "Year",
        "Started Reading",
        "Finished Reading",
        "Owned",
        "Current Page",
    ],
)
books_df = books_df.astype(dtypes_dict)

col1, col2 = st.columns([1, 6], gap="small")

with col1:
    st.metric("Registered Books", value=books_df.shape[0])
    st.metric("Books Owned", value=books_df["Owned"].value_counts().get("Yes", 0))
    st.metric(
        "Read Pages",
        value=books_df["Current Page"].sum(),
        delta=f'{round((books_df["Current Page"].sum()/books_df["Page Count"].sum())*100, 2)}%',
    )
    st.metric("Total Pages", value=books_df["Page Count"].sum())

with col2:
    # Display DataFrame
    st.dataframe(
        books_df,
        use_container_width=True,
        hide_index=True,
        key="books_df",
        column_order=("Title", "Authors", "Description", "Page Count", "Current Page", "Started Reading", "Finished Reading", "Owned"),
        column_config={
            "Title": "Book Title",
            "Authors": "Author(s)",
            "Description": st.column_config.TextColumn(
                max_chars=3,
                width="small",
                help="Click on the row to expand the description.",
            ),
            "Started Reading": st.column_config.DatetimeColumn(
                format="DD/MM/YYYY",
            ),
            "Finished Reading": st.column_config.DatetimeColumn(
                format="DD/MM/YYYY",
            ),
        }
    )
