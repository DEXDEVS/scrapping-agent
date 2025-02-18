# Data Scraper

A web-based data scraper built with Django that allows users to extract text from websites, PDFs, and DOCX files. The extracted data is stored in a database and can be managed through the Django admin panel. Users can also export the data in various formats such as CSV, JSON, and Excel.

## Features

- **Extract text from website URLs** using BeautifulSoup.
- **Extract text from uploaded PDF files** using PyMuPDF.
- **Extract questions and answers** from DOCX tables.
- **Store extracted data in a Django database**.
- **Export data** to CSV, JSON, or Excel formats.
- **User Authentication**: Users can register, log in, and log out.
- **Django Admin Panel**: Manage scraped data and user accounts.

## Installation

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/data-scraper.git
    cd data-scraper
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```

6. Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Default Admin Credentials

- **Username**: `admin`
- **Password**: `admin123`

The default SQLite database is used for development. You can manage the database and view the extracted data through the Django Admin Panel.

To access and manage the database, you can use [DB Browser for SQLite](https://sqlitebrowser.org/) to open and edit the default Django SQLite database (`db.sqlite3`).

## Usage

1. **Login**: Register a new account or log in with your existing credentials.
2. **Scrape Data**: 
    - Enter a website URL to scrape data.
    - Upload a PDF file to extract text.
    - Upload a DOCX file to extract questions and answers.
3. **Export Data**: After scraping, you can export the scraped data in CSV, JSON, or Excel formats.
4. **Manage Data**: The scraped data is stored in the database and can be viewed and managed in the Django admin panel.

## Technologies Used

- **Django**: Web framework for building the app.
- **BeautifulSoup**: For web scraping.
- **PyMuPDF**: For PDF processing.
- **Pandas**: For handling data export to CSV, JSON, and Excel.
- **Bootstrap**: For styling the frontend, including data display tables.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
