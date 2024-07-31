import requests
from requests.exceptions import HTTPError
import os
from pyzbar.pyzbar import decode
from PIL import Image
import isbnlib
import streamlit as st
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

GOOGLE_BOOKS_API_KEY = st.secrets["GOOGLE_BOOKS_API_KEY"]


def get_basic_info(isbn: str):
    """Get a Book's Basic Information.

    Retrieves book information based on the provided ISBN.

    Parameters:
        isbn (str): The ISBN of the book.
    Returns:
        dict: A dictionary containing the book information.

    """
    book_info_unclean = {}
    query = f"isbn:{isbn}"
    print(f"[INFO] TESTING INFO")
    try:
        service = build("books", "v1", developerKey=GOOGLE_BOOKS_API_KEY)
        request = service.volumes().list(q=query)
        res = request.execute()
        if "items" in res:
            book_info_unclean = res["items"][0]["volumeInfo"]
        else:
            return {"error": "No book information found."}
    except HttpError as err:
        if err.resp.status == 403:
            st.error(
                "HTTP error occurred: an HTTP error has occurred (403 Are you making many requests?)"
            )
    except Exception as e:
        st.error(f"An error occurred: {e}")

    book_info = {
        "Title": book_info_unclean.get("title", ""),
        "Authors": book_info_unclean.get("authors", []),
        "Publisher": book_info_unclean.get("publisher", ""),
        "Year": book_info_unclean.get("publishedDate", "").split("-")[0],
        "description": book_info_unclean.get("description", ""),
        "pageCount": book_info_unclean.get("pageCount", ""),
        "categories": book_info_unclean.get("categories", []),
        "averageRating": book_info_unclean.get("averageRating", ""),
        "thumbnail": book_info_unclean.get("thumbnail", ""),
        "infoLink": book_info_unclean.get("infoLink", ""),
    }
    return book_info

with st.form("test_isbn"):
    isbn = st.text_input("Enter the ISBN of the book:", key="isbn")
    submitted = st.form_submit_button("Submit", help="Add a new book to the database.")
    if submitted:
        info = get_basic_info(isbn)
        st.json(info)
