import os
import requests
import fitz  # PyMuPDF
import logging
from bs4 import BeautifulSoup
from docx import Document
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import csv
import json
import pandas as pd
from django.http import HttpResponse
from .models import ScrapedData
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re
from django.shortcuts import get_object_or_404
logger = logging.getLogger("django")

@login_required(login_url='/login/')
def delete_data(request, data_id):
    data_entry = get_object_or_404(ScrapedData, id=data_id, user=request.user)
    data_entry.delete()
    return redirect('/')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect("/login/")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid password")
            return redirect("/login/")

        login(request, user)

        return redirect("/")

    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('/register/')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
        )

        return redirect('/login/')

    return render(request, 'register.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def export_csv(request):
    try:
        source_name = request.GET.get('source_name')
        recent_data = ScrapedData.objects.filter(user=request.user)

        if source_name:
            recent_data = recent_data.filter(source_name=source_name)

        if not recent_data.exists():
            return HttpResponse("No data found", status=404)

        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="filtered_scraped_data.csv"'

        writer = csv.writer(response)
        writer.writerow(['Source Name', 'Content', 'Question', 'Answer'])
        for data in recent_data:
            writer.writerow([data.source_name, data.content, data.question, data.answer])

        return response
    except Exception as e:
        logger.error(f"CSV export failed: {e}", exc_info=True)
        return HttpResponse("Error occurred", status=500)


@login_required(login_url='/login/')
def export_json(request):
    try:
        source_name = request.GET.get('source_name')
        recent_data = ScrapedData.objects.filter(user=request.user)

        if source_name:
            recent_data = recent_data.filter(source_name=source_name)

        if not recent_data.exists():
            return HttpResponse("No data found", status=404)

        response = HttpResponse(json.dumps(list(recent_data.values(
            'source_name', 'content', 'question', 'answer'
        )), indent=4), content_type='application/json')

        response['Content-Disposition'] = 'attachment; filename="filtered_scraped_data.json"'
        return response
    except Exception as e:
        logger.error(f"JSON export failed: {e}", exc_info=True)
        return HttpResponse("Error occurred", status=500)


@login_required(login_url='/login/')
def export_excel(request):
    try:
        source_name = request.GET.get('source_name')
        recent_data = ScrapedData.objects.filter(user=request.user)

        if source_name:
            recent_data = recent_data.filter(source_name=source_name)

        if not recent_data.exists():
            return HttpResponse("No data found", status=404)

        df = pd.DataFrame(list(recent_data.values('source_name', 'content', 'question', 'answer')))

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="filtered_scraped_data.xlsx"'

        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Filtered Data')

        return response
    except Exception as e:
        logger.error(f"Excel export failed: {e}", exc_info=True)
        return HttpResponse("Error occurred", status=500)


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


@login_required(login_url='/login/')
def scrape_data(request):
    latest_scraped_data = None
    source_filter = request.GET.get("source_name")

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to extract data.")
            return redirect("/login/")

        url = request.POST.get("url")
        pdf_file = request.FILES.get("pdf")
        docx_file = request.FILES.get("docx")

        try:
            # Validate URL
            if url:
                url_pattern = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+")
                if not url_pattern.match(url):
                    messages.error(request, "Invalid URL format!")
                    return redirect("/")

                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Extract data from multiple tag types
                    extracted_text = '\n'.join(tag.get_text(strip=True) for tag in soup.find_all(
                        ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div', 'li']))

                    if extracted_text.strip():  # Ensure text is not empty
                        latest_scraped_data = ScrapedData.objects.create(
                            user=request.user,
                            source_name=url,
                            content=extracted_text
                        )
                        messages.success(request, "Website data scraped successfully!")
                    else:
                        messages.error(request, "Not scraped data from this URL.")

            # PDF file processing
            elif pdf_file:
                path = default_storage.save(pdf_file.name, ContentFile(pdf_file.read()))
                doc = fitz.open(default_storage.path(path))
                extracted_text = "\n".join([page.get_text() for page in doc])
                latest_scraped_data = ScrapedData.objects.create(
                    user=request.user,
                    source_name=pdf_file.name,
                    content=extracted_text
                )
                os.remove(default_storage.path(path))  # File delete after processing
                messages.success(request, "PDF data scraped successfully!")

            # DOCX file processing
            elif docx_file:
                path = default_storage.save(docx_file.name, ContentFile(docx_file.read()))
                extracted_data = extract_docx_to_df(default_storage.path(path))
                for item in extracted_data:
                    latest_scraped_data = ScrapedData.objects.create(
                        user=request.user,
                        source_name=docx_file.name,
                        content=f"Q: {item.get('question', 'N/A')}\nA: {item.get('answer', 'N/A')}",
                        question=item.get("question", "N/A"),
                        answer=item.get("answer", "N/A")
                    )
                os.remove(default_storage.path(path))  # File delete after processing
                messages.success(request, "DOCX data scraped successfully!")

            else:
                messages.error(request, "No valid input provided!")
        except Exception as e:
            logger.error(f"Scraping failed: {e}", exc_info=True)
            messages.error(request, "Something went wrong. Please try again.")

    # Filter scraped data based on source name
    scraped_data = ScrapedData.objects.filter(user=request.user).order_by('-created_at')
    if source_filter:
        scraped_data = scraped_data.filter(source_name=source_filter)

    sources = ScrapedData.objects.filter(user=request.user).values_list('source_name', flat=True).distinct()
    return render(request, "index.html", {"data": scraped_data, "sources": sources})
