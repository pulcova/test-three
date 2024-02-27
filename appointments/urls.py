from django.urls import path
from . import views

urlpatterns = [
    path('book-appointment/', views.submit_appointment, name='patient-book-appointment'),
    path('appointment-success/', views.appointment_success, name='appointment-success'),
    path('patient-appointment-list/', views.view_patient_appointments, name='patient-appointment-list'),
    path('patient-calendar/', views.patient_calendar_view, name='patient-calendar'),
    path('doctor-calendar/', views.doctor_calendar_view, name='doctor-calendar'),
    path('staff-calendar/', views.staff_calendar_view, name='staff-calendar'),
]