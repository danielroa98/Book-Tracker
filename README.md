# Book-Tracker

![Book-Tracker](https://img.shields.io/website?url=https%3A%2F%2Fbook-tracker.streamlit.app&up_message=online&up_color=blue&down_message=offline&down_color=red&link=https%3A%2F%2Fbook-tracker.streamlit.app%2F)
![Powered by Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-ff4b4b)

---

Book tracking project that's meant to emulate StoryGraph and GoodReads. Will be used to try to generate insights and custom-made predictions.

## Project Structure

```
.
├── .streamlit/
│   └── secrets.toml
├── pages/
│   ├── 0_scan_a_new_book.py
│   ├── 1_select_a_new_book.py
│   ├── 2_view_books.py
│   ├── 3_select_book.py
│   └── 4_view_stats.py
├── utils/
│   ├── __init__.py
│   ├── assist_functions.py
│   ├── auth.py
│   └── database_funcs.py
├── .env
├── main.py
├── packages.txt
├── README.md
└── requirements.txt
```

__IMPORTANT__: the `.env` and `.streamlit/secrets.toml` files are only referenced in this route path so that other users can visualize where to locate them in their own instances.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/book-tracker.git
    cd book-tracker
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Install system dependencies**:
    ```sh
    sudo apt-get install libzbar0
    ```

## Usage

1. **Run the Streamlit app**:
    ```sh
    streamlit run main.py
    ```

2. **Navigate to the app in your browser**:
    ```
    http://localhost:8501
    ```

## Features

- **Scan a New Book**: Add a new book to the database by scanning its ISBN.
- **Select a New Book**: Choose a book from the database to read.
- **View Books**: View the list of books in the database.
- **Select Book**: Select a book to view its details.
- **View Stats**: View statistics and insights about your reading habits.

## File Descriptions

- **main.py**: Entry point for the Streamlit app.
- **pages/**: Contains the different pages of the Streamlit app.
  - [`0_scan_a_new_book.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fdanielroa%2FLibrary%2FMobile%20Documents%2Fcom~apple~CloudDocs%2FProgramming%2FData-Exploration%2FBook-Tracker%2Fpages%2F0_scan_a_new_book.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/Users/danielroa/Library/Mobile Documents/com~apple~CloudDocs/Programming/Data-Exploration/Book-Tracker/pages/0_scan_a_new_book.py"): Page to scan and add a new book.
  - `1_select_a_new_book.py`: Page to select a new book to read.
  - `2_view_books.py`: Page to view the list of books.
  - `3_select_book.py`: Page to select a book and view its details.
  - `4_view_stats.py`: Page to view statistics and insights.
- **utils/**: Utility functions and classes.
  - `assist_functions.py`: Helper functions for the app.
  - [`auth.py`](command:_github.copilot.openSymbolFromReferences?%5B%22auth.py%22%2C%5B%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22%2FUsers%2Fdanielroa%2FLibrary%2FMobile%20Documents%2Fcom~apple~CloudDocs%2FProgramming%2FData-Exploration%2FBook-Tracker%2FLICENSE%22%2C%22external%22%3A%22file%3A%2F%2F%2FUsers%2Fdanielroa%2FLibrary%2FMobile%2520Documents%2Fcom~apple~CloudDocs%2FProgramming%2FData-Exploration%2FBook-Tracker%2FLICENSE%22%2C%22path%22%3A%22%2FUsers%2Fdanielroa%2FLibrary%2FMobile%20Documents%2Fcom~apple~CloudDocs%2FProgramming%2FData-Exploration%2FBook-Tracker%2FLICENSE%22%2C%22scheme%22%3A%22file%22%7D%2C%22pos%22%3A%7B%22line%22%3A631%2C%22character%22%3A35%7D%7D%2C%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22%2FUsers%2Fdanielroa%2FLibrary%2FMobile%20Documents%2Fcom~apple~CloudDocs%2FProgramming%2FData-Exploration%2FBook-Tracker%2Fpages%2F0_scan_a_new_book.py%22%2C%22external%22%3A%22file%3A%2F%2F%2FUsers%2Fdanielroa%2FLibrary%2FMobile%2520Documents%2Fcom~apple~CloudDocs%2FProgramming%2FData-Exploration%2FBook-Tracker%2Fpages%2F0_scan_a_new_book.py%22%2C%22path%22%3A%22%2FUsers%2Fdanielroa%2FLibrary%2FMobile%20Documents%2Fcom~apple~CloudDocs%2FProgramming%2FData-Exploration%2FBook-Tracker%2Fpages%2F0_scan_a_new_book.py%22%2C%22scheme%22%3A%22file%22%7D%2C%22pos%22%3A%7B%22line%22%3A165%2C%22character%22%3A16%7D%7D%5D%5D "Go to definition"): Authentication-related functions.
  - `database_funcs.py`: Database-related functions.

## License

This project is licensed under the terms of the [`LICENSE`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fdanielroa%2FLibrary%2FMobile%20Documents%2Fcom~apple~CloudDocs%2FProgramming%2FData-Exploration%2FBook-Tracker%2FLICENSE%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/Users/danielroa/Library/Mobile Documents/com~apple~CloudDocs/Programming/Data-Exploration/Book-Tracker/LICENSE") file.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## Contact

For any inquiries, please contact [Daniel Roa](mailto:danielroaglz@gmail.com).
