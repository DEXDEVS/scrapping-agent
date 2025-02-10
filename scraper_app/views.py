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
import csv
import json
import pandas as pd
from django.http import HttpResponse
from .models import ScrapedData

def export_csv(request):
    try:
        recent_id = request.session.get("recent_scraped_id")
        if not recent_id:
            return HttpResponse(status=404)

        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="recent_scraped_data.csv"'

        writer = csv.writer(response)
        writer.writerow(['Source Name', 'Content', 'Question', 'Answer'])

        recent_data = ScrapedData.objects.filter(id=recent_id)
        if not recent_data.exists():
            return HttpResponse(status=404)

        for data in recent_data:
            writer.writerow([data.source_name, data.content, data.question, data.answer])

        return response
    except Exception as e:
        logger.error(f"CSV export failed: {e}", exc_info=True)
        return HttpResponse(status=500)

def export_json(request):
    try:
        recent_id = request.session.get("recent_scraped_id")
        if not recent_id:
            return HttpResponse(status=404)

        recent_data = ScrapedData.objects.filter(id=recent_id).values('source_name', 'content', 'question', 'answer')
        if not recent_data.exists():
            return HttpResponse(status=404)

        response = HttpResponse(json.dumps(list(recent_data), indent=4), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="recent_scraped_data.json"'
        return response
    except Exception as e:
        logger.error(f"JSON export failed: {e}", exc_info=True)
        return HttpResponse(status=500)

def export_excel(request):
    try:
        recent_id = request.session.get("recent_scraped_id")
        if not recent_id:
            return HttpResponse(status=404)

        recent_data = ScrapedData.objects.filter(id=recent_id).values('source_name', 'content', 'question', 'answer')
        if not recent_data.exists():
            return HttpResponse(status=404)

        df = pd.DataFrame(recent_data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="recent_scraped_data.xlsx"'

        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Recent Scraped Data')

        return response
    except Exception as e:
        logger.error(f"Excel export failed: {e}", exc_info=True)
        return HttpResponse(status=500)

# Configure logging
logger = logging.getLogger("django")

def extract_docx_to_df(file_path):
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
            scraped_entry = None  # Variable to store the latest entry

            if url:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    extracted_text = '\n'.join(p.get_text() for p in soup.find_all('p'))
                    scraped_entry = ScrapedData.objects.create(source_name=url, content=extracted_text)
                    messages.success(request, "Website data scraped successfully!")
                else:
                    messages.error(request, f"Error: Unable to scrape website. Status code {response.status_code}")

            elif pdf_file:
                path = default_storage.save(pdf_file.name, ContentFile(pdf_file.read()))
                doc = fitz.open(default_storage.path(path))
                extracted_text = "\n".join([page.get_text() for page in doc])
                scraped_entry = ScrapedData.objects.create(source_name=pdf_file.name, content=extracted_text)
                messages.success(request, "PDF data scraped successfully!")

            elif docx_file:
                path = default_storage.save(docx_file.name, ContentFile(docx_file.read()))
                extracted_data = extract_docx_to_df(default_storage.path(path))
                for item in extracted_data:
                    question = item.get("question", "N/A")
                    answer = item.get("answer", "N/A")
                    scraped_entry = ScrapedData.objects.create(
                        source_name=docx_file.name, content=f"Q: {question}\nA: {answer}",
                        question=question, answer=answer
                    )
                messages.success(request, "DOCX data scraped successfully!")

            else:
                messages.error(request, "No valid input provided!")

            # Store the latest scraped entry ID in session
            if scraped_entry:
                request.session["recent_scraped_id"] = scraped_entry.id

        except Exception as e:
            messages.error(request, f"Something went wrong:")

    return render(request, "index.html")
