from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.docs_dashboard, name='docs_dashboard'),
    path('select-upload-category/', views.select_upload_category, name='select_upload_category'),
    path('upload-report/', views.upload_report, name='upload_report'),
    path('upload-bill/', views.upload_bill, name='upload_bill'),
    path('upload-vaccination/', views.upload_vaccination, name='upload_vaccination'),
    path('upload-prescription/', views.upload_prescription, name='upload_prescription'),

    path('view/prescription/<int:prescription_id>/', views.view_prescription, name='view_prescription'),
    path('view/report/<int:report_id>/', views.view_report, name='view_report'),
    path('view/bill/<int:bill_id>/', views.view_bill, name='view_bill'),
    path('view/vaccination/<int:vaccination_id>/', views.view_vaccination, name='view_vaccination'),

    path('delete/prescription/<int:prescription_id>/', views.delete_prescription, name='delete_prescription'),
    path('delete/bill/<int:bill_id>/', views.delete_bill, name='delete_bill'),
    path('delete/report/<int:report_id>/', views.delete_report, name='delete_report'),
    path('delete/vaccination/<int:vaccination_id>/', views.delete_vaccination, name='delete_vaccination'),

]
