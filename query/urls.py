from django.urls import path
from . import views

urlpatterns = [
    path('patient/', views.patient_queries_list, name='patient-queries-list'),
    path('patient/query/<int:query_id>/', views.patient_query_detail, name='patient-query-detail'),
    path('patient/query/<int:query_id>/delete/', views.patient_delete_query, name='patient-query-delete'),
    path('patient/raise-query/', views.patient_raise_query, name='patient-raise-query'),
    path('queries/update/<int:pk>/', views.PatientQueryUpdateView.as_view(), name='patient-query-update'),

    path('staff/', views.queris_inbox_staff, name='staff-queries-inbox'),
    path('staff/query/<int:query_id>/', views.staff_query_view, name='staff-query-detail'),

    path('doctor/', views.queries_inbox_doctor, name='doctor-queries-inbox'),
    path('doctor/query/<int:query_id>/', views.doctor_query_view, name='doctor-query-detail'),
]