from django.urls import path
from . import views

urlpatterns = [
    path('choose-appointment-slot/', views.choose_appointment_slot, name='choose-appointment-slot'),
    path('patient-appointment-success/', views.patient_appointment_success, name='patient-appointment-success'),
    path('patient-appointment-list/', views.view_patient_appointments, name='patient-appointment-list'),
    path('patient-calendar/', views.patient_calendar_view, name='patient-calendar'),
    path('doctor-calendar/', views.doctor_calendar_view, name='doctor-calendar'),
    path('staff-calendar/', views.staff_calendar_view, name='staff-calendar'),
    path('appointment-booking-form/', views.appointment_booking_form, name='appointment-booking-form')
]