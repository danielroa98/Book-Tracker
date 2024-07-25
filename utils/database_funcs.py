import sqlite3
import os
from typing import Optional, Tuple
from pydantic.dataclasses import dataclass


@dataclass
class BookDatabase:

    # db_name: str
    db_name: str = os.path.join(os.path.dirname(__file__), "..", "books.db")

    def __post_init__(self):
        """
        Performs post-initialization tasks for the class.

        This method is automatically called after the object has been initialized.
        It is used to perform any additional setup or validation that needs to be done.

        Parameters:
            self: The instance of the class.

        Returns:
            None
        """
        self.validate_db_existance()

    def validate_db_existance(self):
        """
        Checks if the database file exists. If not, initializes a new database.

        Returns:
            None
        """
        if not os.path.exists(self.db_name):
            self.init_db(self.db_name)

    def init_db(self, db_name: str) -> str:
        """Initialize Database.

        Initializes the database by creating the 'books' table if it doesn't exist.

        Returns:
            str: A message indicating the status of the initialization process.

        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute(
                """CREATE TABLE IF NOT EXISTS books (
                            isbn TEXT PRIMARY KEY,
                            title TEXT,
                            authors TEXT,
                            publisher TEXT,
                            description TEXT,
                            page_count INTEGER,
                            year INTEGER,
                            started_reading TEXT,
                            ended_reading TEXT,
                            owned TEXT,
                            current_page INTEGER
                    )
                    """
            )
            ret_msg = "Database initialized successfully!"
        except Exception as e:
            ret_msg = f"There was an error!\n\t{e}"
        conn.commit()
        conn.close()
        return ret_msg

    def insert_book(
        self,
        isbn: str,
        title: str,
        authors: str,
        publisher: str,
        description: str,
        page_count: int,
        year: int,
    ) -> str:
        """Insert Book.

        Inserts a new book into the database.

        Args:
            isbn (str): The ISBN of the book.
            title (str): The title of the book.
            authors (str): The authors of the book.
            publisher (str): The publisher of the book.
            description (str): The description of the book.
            page_count (int): The number of pages in the book.
            year (int): The year the book was published.

        Returns:
            str: A message indicating the success or failure of the insertion.

        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute(
                """
                INSERT INTO books (isbn, title, authors, publisher, description, page_count, year, owned, current_page)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'No', 0)
            """,
                (isbn, title, authors, publisher, description, page_count, year),
            )
            ret_msg = f"Book {title} added successfully!"
        except Exception as e:
            ret_msg = f"There was an error!\n\t{e}"
        conn.commit()
        conn.close()
        return ret_msg

    def get_book_by_isbn(
        self,
        isbn: str,
    ) -> Optional[
        Tuple[str, str, str, str, str, int, int, Optional[str], Optional[str], int]
    ]:
        """Get Book by ISBN.

        Retrieves a book from the database based on the given ISBN.

        Args:
            isbn (str): The ISBN of the book to retrieve.

        Returns:
            tuple: A tuple representing the book's information from the database.
                The tuple contains the following fields: (isbn, title, author, year).
                Returns None if no book is found with the given ISBN.

        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
        book = c.fetchone()
        conn.close()
        return book

    def get_book_by_title(
        self,
        title: str,
    ) -> Optional[
        Tuple[str, str, str, str, str, int, int, Optional[str], Optional[str], str, int]
    ]:
        """Get Book.

        Retrieves a book from the database based on the given ISBN.

        Args:
            isbn (str): The ISBN of the book to retrieve.

        Returns:
            tuple: A tuple representing the book's information from the database.
                The tuple contains the following fields: (isbn, title, author, year).
                Returns None if no book is found with the given ISBN.

        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM books WHERE title = ?", (title,))
        book = c.fetchone()
        conn.close()
        return book

    def get_all_books(
        self,
    ) -> Optional[
        Tuple[str, str, str, str, str, int, int, Optional[str], Optional[str], str, int]
    ]:
        """Get All Books.

        Retrieves all books from the database.

        Returns:
            list: A list of tuples representing the books in the database.
                Each tuple contains the book information.

        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM books")
        except Exception as e:
            return f"An error occurred: {e}"
        books = c.fetchall()
        conn.close()
        return books


    def update_book(
        self,
        isbn: str,
        title: str,
        authors: str,
        publisher: str,
        description: str,
        page_count: int,
        year: int,
        started_reading: Optional[str],
        ended_reading: Optional[str],
        owned: str,
        current_page: int,
    ) -> str:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute(
                """
                UPDATE books
                SET title = ?, authors = ?, publisher = ?, description = ?, page_count = ?, year = ?, started_reading = ?, ended_reading = ?, owned = ?, current_page = ?
                WHERE isbn = ?
                """,
                (
                    title,
                    authors,
                    publisher,
                    description,
                    page_count,
                    year,
                    started_reading,
                    ended_reading,
                    owned,
                    current_page,
                    isbn,
                ),
            )
            conn.commit()
            ret_msg = f"{title} with ISBN {isbn} updated successfully!"
        except Exception as e:
            ret_msg = f"An error occurred: {e}"
        conn.close()
        return ret_msg

    def delete_entry(self, isbn: str) -> str:
        """Delete Entry.

        Deletes a book entry from the database based on the provided ISBN.

        Args:
            isbn (str): The ISBN of the book to be deleted.

        Returns:
            str: A message indicating the success or failure of the deletion operation.

        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
            ret_msg = f"Book with ISBN {isbn} deleted successfully!"
        except Exception as e:
            ret_msg = f"An error occurred: {e}"
        conn.close()
        return ret_msg
