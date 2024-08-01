# flake8: noqa
"""Assistance Functions."""
import time

import requests
import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode  # type: ignore
from requests.exceptions import HTTPError

GOOGLE_BOOKS_API_KEY = st.secrets["GOOGLE_BOOKS_API_KEY"]


def get_basic_info(isbn: str) -> dict | None:
    """Get a Book's Basic Information.

    Retrieves book information based on the provided ISBN.

    Parameters:
        isbn (str): The ISBN of the book.
    Returns:
        dict: A dictionary containing the book information.

    """
    book_info_unclean = {}
    query = f"isbn:{isbn}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}&country=MX"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            print("[INFO] Found a book's information!")
            data = res.json()
            if "items" in data:
                book_info_unclean = data["items"][0]["volumeInfo"]
    except HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
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


def scan_barcode(image: Image) -> str | None:  # type: ignore
    """Scan Barcode.

    Scans a barcode image and returns the decoded barcode data.

    Args:
        image: The barcode image to be scanned.

    Returns:
        The decoded barcode data as a string, or None if no barcode is found.
    """
    barcodes = decode(image)
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        return barcode_data
    return None
