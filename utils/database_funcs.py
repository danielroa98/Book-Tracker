import os
import sqlite3
from typing import Optional, Tuple, List

from pydantic.dataclasses import dataclass


@dataclass
class BookDatabase:
    db_name: str = os.path.join(os.path.dirname(__file__), "..", "books.db")
    bookshelf_db: str = os.path.join(os.path.dirname(__file__), "..", "bookshelf.db")

    def __post_init__(self):
        self.validate_db_existance()

    def validate_db_existance(self):
        if not os.path.exists(self.db_name):
            self.init_db(self.db_name)
        if not os.path.exists(self.bookshelf_db):
            self.init_bookshelf_db(self.bookshelf_db)

    def init_db(self, db_name: str) -> str:
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

    def attach_bookshelf_db(self, conn):
        conn.execute("ATTACH DATABASE ? AS bookshelf_db", (self.bookshelf_db,))

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
    ) -> Optional[
        Tuple[str, str, str, str, str, int, int, Optional[str], Optional[str], int]
    ]:
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
    ) -> Optional[
        Tuple[str, str, str, str, str, int, int, Optional[str], Optional[str], str, int]
    ]:
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
    ) -> Optional[
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
    ]:
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

    def get_from_bookshelf(self, username: str) -> Optional[list[Tuple]]:
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

    def get_one_book_bookshelf(self, book_id: str, owner: str) -> Optional[Tuple]:
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
                cursor.execute("DELETE FROM bookshelf WHERE isbn = ? AND owner = ?", (book_id, username))
                return f"Book with ISBN {book_id} removed from your bookshelf!"
        except Exception as e:
            return f"An error occurred: {e}\n\tRemove From Bookshelf"
