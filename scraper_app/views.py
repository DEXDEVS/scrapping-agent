import os
import requests
import fitz  # PyMuPDF
import logging
from bs4 import BeautifulSoup
from docx import Document
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
from .models import ScrapedData

# Configure logging
logger = logging.getLogger("django")


def extract_docx_to_df(file_path):
    """
    Extracts data from a DOCX file where each table contains two rows:
    - Row 1: Question
    - Row 2: Answer
    """
    document = Document(file_path)
    data = []
    for table in document.tables:
        if len(table.rows) < 2:
            continue
        question = " ".join(cell.text.strip() for cell in table.rows[0].cells)
        answer = " ".join(cell.text.strip() for cell in table.rows[1].cells)
        data.append({"question": question, "answer": answer})
    return data


def scrape_data(request):
    if request.method == "POST":
        url = request.POST.get("url")
        pdf_file = request.FILES.get("pdf")
        docx_file = request.FILES.get("docx")

        try:
            if url:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    extracted_text = '\n'.join(p.get_text() for p in soup.find_all('p'))
                    ScrapedData.objects.create(source_name=url, content=extracted_text)
                    messages.success(request, "Website data scraped successfully!")
                else:
                    error_message = f"Error: Unable to scrape website. Status code {response.status_code}"
                    messages.error(request, error_message)
                    logger.error(error_message)  # Log the error

            elif pdf_file:
                path = default_storage.save(pdf_file.name, ContentFile(pdf_file.read()))
                doc = fitz.open(default_storage.path(path))
                extracted_text = "\n".join([page.get_text() for page in doc])
                ScrapedData.objects.create(source_name=pdf_file.name, content=extracted_text)
                messages.success(request, "PDF data scraped successfully!")

            elif docx_file:
                path = default_storage.save(docx_file.name, ContentFile(docx_file.read()))
                extracted_data = extract_docx_to_df(default_storage.path(path))
                for item in extracted_data:
                    question = item.get("question", "N/A")
                    answer = item.get("answer", "N/A")
                    ScrapedData.objects.create(source_name=docx_file.name, content=f"Q: {question}\nA: {answer}",
                                               question=question, answer=answer)
                messages.success(request, "DOCX data scraped successfully!")
            else:
                error_message = "No valid input provided!"
                messages.error(request, error_message)
                logger.error(error_message)  # Log the error
        except Exception as e:
            error_message = f"Something went wrong: {str(e)}"
            messages.error(request, error_message)
            logger.error(error_message)  # Log the exception

    return render(request, "index.html")
