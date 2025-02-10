from django.urls import path
from .views import scrape_data, export_csv, export_json, export_excel

urlpatterns = [
    path('', scrape_data, name='scrape_data'),
    path('export/csv/', export_csv, name='export_csv'),
    path('export/json/', export_json, name='export_json'),
    path('export/excel/', export_excel, name='export_excel'),
]
