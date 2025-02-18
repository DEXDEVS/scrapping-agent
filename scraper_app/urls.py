from django.urls import path
from .views import scrape_data, export_csv, export_json, export_excel, login_page, register, logout_page, delete_data


urlpatterns = [
    path('', scrape_data, name='scrape_data'),
    path('export/csv/', export_csv, name='export_csv'),
    path('export/json/', export_json, name='export_json'),
    path('export/excel/', export_excel, name='export_excel'),
    path('login/', login_page, name='login_page'),
    path('register/', register, name='register'),
    path('logout/', logout_page, name='logout_page'),
    path('accounts/login/', login_page, name='default_login'),
    path('delete/<int:data_id>/', delete_data, name='delete_data'),

]
