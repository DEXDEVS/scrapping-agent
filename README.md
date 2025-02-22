# Data Scraper

A web-based data scraper built with Django that allows users to extract text from websites, PDFs, and DOCX files. The extracted data is stored in a database and can be managed through the Django admin panel. Users can also apply filters, selectively export data using checkboxes, and download the data in various formats such as CSV, JSON, and Excel.
## Features

* Extract text from website URLs using BeautifulSoup.
* Extract text from uploaded PDF files using PyMuPDF.
* Extract questions and answers from DOCX tables.
* Store extracted data in a Django database.
* Apply filters based on source name before exporting.
* Export specific rows using checkboxes or download the entire dataset.
* Export data to CSV, JSON, or Excel formats.
* User Authentication: Users can register, log in, and log out.
* Django Admin Panel: Manage scraped data and user accounts.
* Bootstrap UI: Enhanced front-end with Bootstrap styling for improved UX.


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
5. Collect static files:

    ```bash
    python manage.py collectstatic
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```

6. Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Default Admin Credentials

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
3. **Export Data**: 
    - Use filters to refine results based on source name.
    - Select specific rows via checkboxes or export all data.
    - Export scraped data in CSV, JSON, or Excel formats.
4. **Manage Data**: The scraped data is stored in the database and can be viewed and managed in the Django admin panel.


## Technologies Used

- **Django**: Web framework for building the app.
- **BeautifulSoup**: For web scraping.
- **PyMuPDF**: For PDF processing.
- **Pandas**: For handling data export to CSV, JSON, and Excel.
- **Bootstrap**: For styling the frontend, including data display tables.

## Troubleshooting

1. **Static Files Not Loading?**

_**python manage.py collectstatic**_

Ensure your STATIC_URL and STATICFILES_DIRS are correctly set in settings.py.

2. **Database Issues?**

**_python manage.py migrate --run-syncdb_**

3. **Permission Errors?**

Ensure db.sqlite3 and static folders have the correct permissions.

## Contributing

Fork the repository, create a new feature or bugfix branch, and submit a pull request.
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

