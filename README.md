# Data Scraper

A simple web application built with Django that allows users to scrape text data from a website URL or extract text from a PDF file.

## Features
- Scrapes text from any given website URL.
- Extracts text content from uploaded PDF files.
- Saves extracted data in a database.
- Uses `BeautifulSoup` for web scraping.
- Uses `PyMuPDF` for processing PDF files.
- Built with Bootstrap for a clean UI.

## Installation

### Prerequisites
- Python 
- Django 
- Virtual environment 

### Setup

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/data-scraper.git
   cd data-scraper
   
2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies
pip install -r requirements.txt

4. Run migrations
python manage.py migrate 

5. Start the server
python manage.py runserver
Open http://127.0.0.1:8000/ in your browser. 

6. Usage
-Enter a website URL and click "Scrape" to extract text.
-Upload a PDF file and click "Scrape" to extract text from the document.
-Extracted text is stored in the database.