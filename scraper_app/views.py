import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import ScrapedData


def scrape_data(request):
    extracted_text = ""
    if request.method == "POST":
        url = request.POST.get("url")
        pdf_file = request.FILES.get("pdf")

        if url:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                extracted_text = '\n'.join(p.get_text() for p in soup.find_all('p'))
                print("Website text extracted successfully!")
            else:
                extracted_text = "Failed to retrieve website content."
                print(f"Error: {response.status_code}")

        elif pdf_file:
            path = default_storage.save(pdf_file.name, ContentFile(pdf_file.read()))
            doc = fitz.open(default_storage.path(path))
            extracted_text = "\n".join([page.get_text() for page in doc])
            print("PDF text extracted successfully!")

        if extracted_text:
            ScrapedData.objects.create(content=extracted_text)
            print("Extracted data saved to the database!")

    return render(request, "index.html")
