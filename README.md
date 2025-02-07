Data Scraper
A web-based data scraper built with Django that allows users to extract text from websites, PDFs, and DOCX files. The extracted data is stored in a database and can be managed through the Django admin panel.

**Features**
Extract text from website URLs using BeautifulSoup.
Extract text from uploaded PDF files using PyMuPDF.
Extract questions and answers from DOCX tables.
Store extracted data in a Django database.
Django admin panel for managing scraped data.

**Installation**

1- Clone the repository:
git clone https://github.com/yourusername/data-scraper.git  
cd data-scraper  
2- Create a virtual environment and activate it:
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  
3- Install dependencies:
pip install -r requirements.txt  
4- Apply migrations:
python manage.py migrate  
5- Run the development server:
python manage.py runserver  
Access the app at http://127.0.0.1:8000/

**Usage**
Enter a website URL, upload a PDF, or upload a DOCX file.
Click the Scrape button to extract data.
Extracted data is stored in the database and can be viewed in the Django admin panel.
**Technologies Used**
Django
BeautifulSoup (for web scraping)
PyMuPDF (for PDF processing)
python-docx (for DOCX file extraction)
Bootstrap (for frontend styling)
**License**
This project is licensed under the MIT License.

