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
    query_parts = []
    if book_info.get("Title"):
        query_parts.append(f"intitle:{book_info.get('Title')}")
    if book_info.get("Authors"):
        for author in book_info.get("Authors"):
            query_parts.append(f"inauthor:{author}")
    if book_info.get("Publisher"):
        query_parts.append(f"inpublisher:{book_info.get('Publisher')}")
    if book_info.get("Year"):
        query_parts.append(f"year:{book_info.get('Year')}")
    if book_info.get("Language"):
        query_parts.append(f"lang:{book_info.get('Language')}")

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
    print(f"[INFO] Key is: {GOOGLE_BOOKS_API_KEY}")
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"
    try:
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
    except HTTPError as http_err:
        if res.status_code == 403:
            st.error(
                "HTTP error occurred: an HTTP error has occurred (403 Are you making many requests?)"
            )
            time.sleep(60)  # Wait for 60 seconds before retrying
            return get_google_books_info(query)
        else:
            st.error(f"HTTP error occurred: {http_err}")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
    return None


def get_google_books_info_simplified(query: str) -> dict | None:
    try:
        service = build("books", "v1", developerKey=GOOGLE_BOOKS_API_KEY)
        request = service.volumes().list(q=query)
        response = request.execute()
        if "items" in response:
            return response["items"][0]["volumeInfo"]
        else:
            return {}
    except HttpError as e:
        if e.resp.status == 403 and "unknownLocation" in str(e):
            # Attempt to retry with a specified IP header for geolocation
            url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"
            headers = {"X-Forwarded-For": "8.8.8.8"}  # Example IP address
            try:
                res = requests.get(url, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    if "items" in data:
                        return data["items"][0]["volumeInfo"]
                    else:
                        return {}
                else:
                    st.error(f"HTTP error occurred: {res.status_code} - {res.text}")
            except Exception as retry_err:
                st.error(f"Retry error occurred: {retry_err}")
        else:
            st.error(f"Google Books API error: {e}")
        return {}


# def get_google_books_info_simplified(query: str) -> dict | None:
#     service = build("books", "v1", developerKey=GOOGLE_BOOKS_API_KEY)
#     request = service.volumes().list(q=query)
#     response = request.execute()
#     if "items" in response:
#         return response["items"][0]["volumeInfo"]
#     else:
#         return {}


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
