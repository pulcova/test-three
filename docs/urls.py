from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.docs_dashboard, name='docs_dashboard'),
    path('select-upload-category/', views.select_upload_category, name='select_upload_category'),
    path('upload-report/', views.upload_report, name='upload_report'),
    path('upload-bill/', views.upload_bill, name='upload_bill'),
    path('upload-vaccination/', views.upload_vaccination, name='upload_vaccination'),
    path('upload-prescription/', views.upload_prescription, name='upload_prescription'),
]
