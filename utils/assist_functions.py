import requests
import os
from pyzbar.pyzbar import decode
from PIL import Image
import isbnlib
import streamlit as st

GOOGLE_BOOKS_API_KEY = st.secrets["GOOGLE_BOOKS_API_KEY"]


def build_google_books_query(book_info: dict) -> str:
    """Build Google Books Query.

    Builds a query string for searching books on Google Books API based on the provided book information.

    Args:
        book_info (dict): A dictionary containing the book information.
            The dictionary should have the following keys:
            - "Title" (str): The title of the book.
            - "Authors" (list): A list of authors of the book.
            - "Publisher" (str): The publisher of the book.
            - "Year" (str): The year of publication of the book.
            - "Language" (str): The language of the book.

    Returns:
        str: The query string for searching books on Google Books API.

    Example:
        >>> book_info = {
        ...     "Title": "The Great Gatsby",
        ...     "Authors": ["F. Scott Fitzgerald"],
        ...     "Publisher": "Scribner",
        ...     "Year": "1925",
        ...     "Language": "English"
        ... }
        >>> build_google_books_query(book_info)
        'intitle:The+Great+Gatsby+inauthor:F.+Scott+Fitzgerald+inpublisher:Scribner+year:1925+lang:English'

    """
    title = book_info.get("Title")
    authors = book_info.get("Authors")
    publisher = book_info.get("Publisher")
    year = book_info.get("Year")
    language = book_info.get("Language")
    query_parts = []
    if title:
        query_parts.append(f"intitle:{title}")
    if authors:
        for author in authors:
            query_parts.append(f"inauthor:{author}")
    if publisher:
        query_parts.append(f"inpublisher:{publisher}")
    if year:
        query_parts.append(f"year:{year}")
    if language:
        query_parts.append(f"lang:{language}")

    query = "+".join(query_parts)
    return query


def get_google_books_info(query: str) -> dict | None:
    """Get Google Books Information.
    Retrieves information about a book from the Google Books API.

    Args:
        query (str): The search query for the book.

    Returns:
        dict | None: A dictionary containing the book's information if found, or None if no information is found.

    """
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"
    res = requests.get(url)
    if res.status_code == 200:
        print(f"[INFO] Found a book's information!")
        data = res.json()
        if "items" in data:
            vol_info = data["items"][0]["volumeInfo"]
            return {
                "title": vol_info.get("title", "N/A"),
                "authors": ", ".join(vol_info.get("authors", [])),
                "publisher": vol_info.get("publisher", "N/A"),
                "publishedDate": vol_info.get("publishedDate", "N/A"),
                "description": vol_info.get("description", "N/A"),
                "pageCount": vol_info.get("pageCount", "N/A"),
                "categories": ", ".join(vol_info.get("categories", [])),
                "averageRating": vol_info.get("averageRating", "N/A"),
                "thumbnail": vol_info.get("imageLinks", {}).get("thumbnail", "N/A"),
                "infoLink": vol_info.get("infoLink", "N/A"),
            }
    else:
        print(f"[ERROR] No book information found.")
        return None


def scan_barcode(image) -> str | None:
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


def get_basic_info(isbn: str):
    """Get a Book's Basic Information.

    Retrieves book information based on the provided ISBN.

    Parameters:
        isbn (str): The ISBN of the book.

    Returns:
        dict: A dictionary containing the book information.
    """
    book_info = {}
    try:
        book_info = isbnlib.meta(isbn)
    except isbnlib.dev._exceptions.ISBNLibHTTPError as e:
        st.error(f"HTTP error occurred: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    return book_info
