import io

import streamlit as st
from PIL import Image

import utils.assist_functions as af
from utils.database_funcs import BookDatabase

# Global Variables
BOOK_INFO: dict = {}
MORE_BOOK_INFO: dict = {}

GOOGLE_BOOKS_API_KEY = st.secrets["GOOGLE_BOOKS_API_KEY"]

st.set_page_config(
    page_title="Add a new book",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Add a new book📚")

db = BookDatabase("books.db")

# Prompt the user to choose an option: upload an image or take a picture
option = st.radio("Choose an option:", ("Upload an image", "Take a picture"))

image = None

if option == "Upload an image":
    # Allow the user to upload an image file
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Open the uploaded image file
        image = Image.open(uploaded_file)
elif option == "Take a picture":
    # Allow the user to take a picture using the camera
    cam_image = st.camera_input("Take a picture of the book's barcode.")
    if cam_image is not None:
        # Open the captured image from the camera
        image = Image.open(io.BytesIO(cam_image.getvalue()))

with st.container(border=True):
    if image:
        # Display the scanned barcode image
        st.image(image, caption="Scanned Barcode", use_column_width=True)
        st.write("\nScanning barcode...")

        # Scan the barcode in the image and retrieve the ISBN
        isbn = af.scan_barcode(image)
        if isbn:
            # Display the scanned ISBN
            st.write(f"ISBN: {isbn}")
            # Get book information based on the ISBN
            BOOK_INFO = af.get_basic_info(isbn)
            if BOOK_INFO:
                # Display the book information
                st.write("Book Information:")
                st.write(BOOK_INFO)
            else:
                # Inform the user that no information is found for the ISBN
                st.write("No information found for this ISBN.")
            with st.expander(label="View Additional Information"):
                # Get more book information based on a Google Books API query
                # Display the book information
                st.write("Book Information:")
                st.write(MORE_BOOK_INFO)
        else:
            # Inform the user that no barcode is found in the image
            st.write("No barcode found in the image.")

# Add the book to the database
st.divider()

if BOOK_INFO:
    st.subheader("Do you want to add this book to your database?")
    st.text("Please confirm the details before adding the book.")

    with st.form("add_book"):
        pages = 0
        description = ""
        insert_msg = ""

        col1, col2 = st.columns(2)
        desc1, desc2, desc3 = st.columns([1, 3, 1])
        ord1, ord2, ord3 = st.columns(3)

        with col1:
            title = st.text_input(
                "Book Title",
                value=BOOK_INFO.get("Title", ""),
                placeholder="Enter the book's title.",
            )
            authors = st.text_input(
                "Authors",
                value=", ".join(BOOK_INFO.get("Authors", [])),
                placeholder="Enter the name(s) of the author(s) of the book.",
            )
            publisher = st.text_input(
                "Publisher",
                value=BOOK_INFO.get("Publisher", ""),
                placeholder="Enter the publisher of the book.",
            )

        with col2:
            isbn = st.text_input(
                "ISBN",
                value=isbn,
                placeholder="Enter the ISBN of the book.",
                disabled=True,
            )
            year = st.text_input(
                "Year",
                value=BOOK_INFO.get("Year", ""),
                placeholder="Enter the year of publication.",
            )
            pages = st.number_input(
                "Pages",
                value=BOOK_INFO.get("pageCount", ""),
                placeholder="Enter the number of pages in the book.",
                min_value=0,
                step=1,
            )

        with desc2:
            description = st.text_area(
                "Description",
                value=BOOK_INFO.get("description", ""),
                placeholder="Enter a brief description of the book.",
            )

        with ord2:
            submitted = st.form_submit_button(
                "Submit", help="Add a new book to the database."
            )
            if submitted:
                insert_msg = db.insert_book(
                    isbn=isbn,
                    title=title,
                    authors=authors,
                    publisher=publisher,
                    description=description,
                    page_count=int(pages),
                    year=int(year),
                )
                if "successfully" in insert_msg:
                    st.success(insert_msg)
                else:
                    st.error(insert_msg)
