# flake8: noqa
"""Database Functions."""

import os
import sqlite3
from typing import List, Optional, Tuple

from pydantic.dataclasses import dataclass


@dataclass
class BookDatabase:
    """
    A class representing a book database.

    Attributes:
        db_name (str): The path to the main books database file.
        bookshelf_db (str): The path to the bookshelf database file.

    Methods:
        - __post_init__(): Initializes the book database by validating its existence.
        - validate_db_existence(): Validates the existence of the main books database and the bookshelf database.
        - init_db(db_name: str) -> str: Initializes the main books database by creating the necessary table.
        - init_bookshelf_db(db_name: str) -> str: Initializes the bookshelf database by creating the necessary table.
        - attach_bookshelf_db(conn): Attaches the bookshelf database to the main books database connection.
        - insert_book(isbn: str, title: str, authors: str, publisher: str, description: str, page_count: int, year: int) -> str: Inserts a new book into the database.
        - get_book_by_isbn(isbn: str) -> Optional[Tuple]: Retrieves a book from the database based on its ISBN.
        - get_book_by_title(title: str) -> Optional[Tuple]: Retrieves a book from the database based on its title.
        - get_all_books() -> Optional[List[Tuple]]: Retrieves all books from the database.Optional[str], owned: str, current_page: int) -> str: Updates the information of a book in the database.
        - delete_entry(isbn: str) -> str: Deletes a book from the database based on its ISBN.
        - add_to_bookshelf(book_id: str, username: str) -> str: Adds a book to the user's bookshelf.
        - get_from_bookshelf(username: str) -> Optional[List[Tuple]]: Retrieves all books from the user's bookshelf.
        - get_one_book_bookshelf(book_id: str, owner: str) -> Optional[Tuple]: Retrieves a specific book from the user's bookshelf.
    """

    db_name: str = os.path.join(os.path.dirname(__file__), "..", "books.db")
    bookshelf_db: str = os.path.join(os.path.dirname(__file__), "..", "bookshelf.db")

    def __post_init__(self) -> None:
        """
        Performs post-initialization tasks for the class.

        This method is automatically called after the object has been initialized.
        It is used to perform any additional setup or validation tasks.

        Returns:
            None
        """
        self.validate_db_existence()

    def validate_db_existence(self) -> None:
        """
        Checks if the database and bookshelf database exist.
        If they don't exist, initializes them.
        """
        if not os.path.exists(self.db_name):
            self.init_db(self.db_name)
        if not os.path.exists(self.bookshelf_db):
            self.init_bookshelf_db(self.bookshelf_db)

    def init_db(self, db_name: str) -> str:
        """
        Initializes the books database by creating the necessary table if it doesn't exist.

        Args:
            db_name (str): The name of the database.

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
            ret_msg = f"There was an error initializing the books database!\n\t{e}"
        conn.commit()
        conn.close()
        return ret_msg

    def init_bookshelf_db(self, db_name: str) -> str:
        """
        Initializes the bookshelf database with the given name.

        Args:
            db_name (str): The name of the bookshelf database.

        Returns:
            str: A message indicating the success or failure of the initialization.
        """
        conn = sqlite3.connect(self.bookshelf_db)
        c = conn.cursor()
        try:
            c.execute("PRAGMA foreign_keys = ON;")
            c.execute(
                """CREATE TABLE IF NOT EXISTS bookshelf (
                            isbn TEXT PRIMARY KEY,
                            owner TEXT,
                            FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE,
                            FOREIGN KEY (owner) REFERENCES users(username) ON DELETE CASCADE
                    )
                    """
            )
            ret_msg = f"Bookshelf Database with name {self.bookshelf_db} initialized successfully!"
        except Exception as e:
            ret_msg = f"There was an error initializing the bookshelf database!\n\t{e}"
        conn.commit()
        conn.close()
        return ret_msg

    def attach_bookshelf_db(self, conn: sqlite3.connect) -> None:  # type: ignore
        """
        Attaches the bookshelf database to the given connection.

        Parameters:
        conn (sqlite3.connect): The connection to the main database.

        Returns:
        None
        """
        conn.execute("ATTACH DATABASE ? AS bookshelf_db", (self.bookshelf_db,))  # type: ignore

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
        """
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
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'Yes', 0)
            """,
                (isbn, title, authors, publisher, description, page_count, year),
            )
            ret_msg = f"Book {title} added successfully!"
        except Exception as e:
            ret_msg = f"There was an error inserting the book!\n\t{e}"
        finally:
            conn.commit()
            conn.close()
            return ret_msg

    def get_book_by_isbn(
        self,
        isbn: str,
    ) -> (
        Optional[
            Tuple[str, str, str, str, str, int, int, Optional[str], Optional[str], int]
        ]
        | str
    ):
        """
        Retrieves a book from the database based on its ISBN.

        Args:
            isbn (str): The ISBN of the book to retrieve.

        Returns:
            Optional[Tuple[str, str, str, str, str, int, int, Optional[str], Optional[str], int]] or str:
                If the book is found, a tuple containing the book's information is returned.
                If the book is not found, a string indicating an error is returned.
        """
        conn = sqlite3.connect(self.db_name)
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
            book = c.fetchone()
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()
            return book

    def get_book_by_title(
        self,
        title: str,
    ) -> (
        Optional[
            Tuple[
                str,
                str,
                str,
                str,
                str,
                int,
                int,
                Optional[str],
                Optional[str],
                str,
                int,
            ]
        ]
        | str
    ):
        """
        Retrieves a book from the database based on its title.

        Args:
            title (str): The title of the book to retrieve.

        Returns:
            Optional[Tuple[str, str, str, str, str, int, int, Optional[str], Optional[str], str, int]] or str:
            - If a book with the given title is found, returns a tuple containing the book's information.
            - If no book is found, returns None.
            - If an error occurs during the retrieval process, returns an error message as a string.
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM books WHERE title = ?", (title,))
            book = c.fetchone()
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()
            return book

    def get_all_books(
        self,
    ) -> (
        Optional[
            List[
                Tuple[
                    str,
                    str,
                    str,
                    str,
                    str,
                    int,
                    int,
                    Optional[str],
                    Optional[str],
                    str,
                    int,
                ]
            ]
        ]
        | str
    ):
        """
        Retrieve all books from the database.

        Returns:
            Optional[List[Tuple[str, str, str, str, str, int, int, Optional[str], Optional[str], str, int]]]:
            A list of tuples representing the books. Each tuple contains the following information:
            - Title (str)
            - Author (str)
            - Publisher (str)
            - Publication Date (str)
            - ISBN (str)
            - Pages (int)
            - Rating (int)
            - Review (Optional[str])
            - Notes (Optional[str])
            - Genre (str)
            - Read Status (int)

            If an error occurs during the retrieval, None is returned.
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM books")
            books = c.fetchall()
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
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
        finally:
            conn.close()
            return ret_msg

    def delete_entry(self, isbn: str) -> str:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        ret_msg = ""
        try:
            c.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
            ret_msg = f"Book with ISBN {isbn} deleted successfully!"
        except Exception as e:
            ret_msg = f"An error occurred: {e}"
        finally:
            conn.close()
        return ret_msg

    def add_to_bookshelf(self, book_id: str, username: str) -> str:
        conn = sqlite3.connect(self.db_name)
        self.attach_bookshelf_db(conn)
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO bookshelf_db.bookshelf (isbn, owner) VALUES (?, ?)",
                (book_id, username),
            )
            conn.commit()
            return f"Book with ISBN {book_id} added to your bookshelf!"
        except Exception as e:
            return f"An error occurred: {e}\n\tAdd To Bookshelf"
        finally:
            conn.close()

    def get_from_bookshelf(self, username: str) -> Optional[list[Tuple]] | str:
        try:
            with sqlite3.connect(self.bookshelf_db) as bookshelf_conn:
                bookshelf_conn.execute(f"ATTACH DATABASE '{self.db_name}' AS books_db")
                cursor = bookshelf_conn.cursor()
                cursor.execute(
                    """
                    SELECT
                        books_db.books.isbn,
                        books_db.books.title,
                        books_db.books.authors,
                        books_db.books.publisher,
                        books_db.books.description,
                        books_db.books.page_count,
                        books_db.books.year,
                        books_db.books.started_reading,
                        books_db.books.ended_reading,
                        books_db.books.owned,
                        books_db.books.current_page
                    FROM bookshelf
                    INNER JOIN books_db.books ON bookshelf.isbn = books_db.books.isbn
                    WHERE owner = ?
                    """,
                    (username,),
                )
                books = cursor.fetchall()
        except Exception as e:
            return f"An error occurred: {e}\n\tGet From Bookshelf"
        return books

    def get_one_book_bookshelf(self, book_id: str, owner: str) -> Optional[Tuple] | str:
        try:
            with sqlite3.connect(self.bookshelf_db) as bookshelf_conn:
                bookshelf_conn.execute(f"ATTACH DATABASE '{self.db_name}' AS books_db")
                cursor = bookshelf_conn.cursor()
                cursor.execute(
                    """
                    SELECT
                        books_db.books.isbn,
                        books_db.books.title,
                        books_db.books.authors,
                        books_db.books.publisher,
                        books_db.books.description,
                        books_db.books.page_count,
                        books_db.books.year,
                        books_db.books.started_reading,
                        books_db.books.ended_reading,
                        books_db.books.owned,
                        books_db.books.current_page
                    FROM bookshelf
                    INNER JOIN books_db.books ON bookshelf.isbn = books_db.books.isbn
                    WHERE bookshelf.isbn = ? AND bookshelf.owner = ?
                    """,
                    (book_id, owner),
                )
                book = cursor.fetchone()
        except Exception as e:
            return f"An error occurred: {e}\n\tGet One Book Bookshelf"
        return book

    def remove_from_bookshelf(self, book_id: str, username: str) -> str:
        try:
            with sqlite3.connect(self.bookshelf_db) as bookshelf_conn:
                cursor = bookshelf_conn.cursor()
                cursor.execute(
                    "DELETE FROM bookshelf WHERE isbn = ? AND owner = ?",
                    (book_id, username),
                )
                return f"Book with ISBN {book_id} removed from your bookshelf!"
        except Exception as e:
            return f"An error occurred: {e}\n\tRemove From Bookshelf"
