from django.shortcuts import render
from users.models import Doctor
from users.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, time
from django.shortcuts import render, redirect, get_object_or_404

from  users.models import Patient, Doctor
from .models import Appointment, Slot
from .forms import PatientAppointmentForm, PatientAppointmentUpdateForm
from users.decorators import allowed_users
from datetime import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def convert_to_24_hour_format(time_str):
    time_obj = datetime.strptime(time_str, '%I:%M %p')
    return time_obj.strftime('%H:%M:%S')

def send_appointment_confirmation_email(appointment):
    subject = 'Appointment Confirmation'
    context = {
        'appointment': appointment,
        'doctor': appointment.doctor,
        'patient': appointment.patient,
    }
    message_plain = render_to_string('appointments/appointment_confirmation_email.txt', context)
    message_html = render_to_string('appointments/appointment_confirmation_email.html', context)

    send_mail(
        subject,
        message_plain,
        settings.EMAIL_HOST_USER,  
        [appointment.patient.email],  
        html_message=message_html,
    )

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def choose_appointment_slot(request):  
    doctors = Doctor.objects.all()
    selected_doctor = None
    slots = []

    if request.method == 'POST':
        if 'doctor' in request.POST:
            doctor_id = request.POST.get('doctor')
            selected_doctor = Doctor.objects.get(id=doctor_id)

            selected_date_str = request.POST.get('date')
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()

            slots = Slot.objects.filter(doctor=selected_doctor, date=selected_date)

    return render(request, 'appointments/choose_appointment_slot.html', {'doctors': doctors, 'selected_doctor': selected_doctor, 'slots': slots})

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def appointment_booking_form(request):
    if request.method == 'GET':
        start_time = request.GET.get('start_time').replace('a.m.', 'AM').replace('p.m.', 'PM')
        end_time = request.GET.get('end_time').replace('a.m.', 'AM').replace('p.m.', 'PM')

        if start_time.lower() == 'noon':
            start_time = '12:00 PM'
        elif start_time.lower() == 'midnight':
            start_time = '12:00 AM'

        if end_time.lower() == 'noon':
            end_time = '12:00 PM'
        elif end_time.lower() == 'midnight':
            end_time = '12:00 AM'

        if ":" not in start_time and ("AM" in start_time or "PM" in start_time):
            start_time = start_time.replace(" AM", ":00 AM").replace(" PM", ":00 PM")
        if ":" not in end_time and ("AM" in end_time or "PM" in end_time):
            end_time = end_time.replace(" AM", ":00 AM").replace(" PM", ":00 PM")

        start_time = convert_to_24_hour_format(start_time)
        end_time = convert_to_24_hour_format(end_time)

        date = request.GET.get('date')
        doctor_id = request.GET.get('doctor_id')  
        doctor = Doctor.objects.get(id=doctor_id)  
        user_patient = Patient.objects.get(user=request.user)  
        form = PatientAppointmentForm(initial={'start_time': start_time, 'end_time': end_time, 'date': date, 'doctor': doctor, 'patient': user_patient})
        return render(request, 'appointments/appointment_booking_form.html', {'form': form})
    elif request.method == 'POST':
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)

            slot = Slot.objects.get(doctor=appointment.doctor, date=appointment.date, start_time=appointment.start_time, end_time=appointment.end_time)

            slot.is_available = False
            slot.patient = appointment.patient
            slot.save()

            appointment.save()

            send_appointment_confirmation_email(appointment)
            return redirect('patient-appointment-success')
        else:
            print("Form is invalid!")  
            print(form.errors) 
    return render(request, 'appointments/appointment_booking_form.html', {'form': form})


@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def patient_appointment_success(request):
    return render(request, 'appointments/patient_appointment_success.html')

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def patient_calendar_view(request):
    user = request.user
    patient = get_object_or_404(Patient, user=user)
    patient_appointments = Appointment.objects.filter(patient=patient, date__isnull=False)
    
    serialized_appointments = [{
        'title': appointment.reason,  
        'start': datetime.combine(appointment.date, appointment.start_time).strftime('%Y-%m-%dT%H:%M:%S') if appointment.date and appointment.start_time else None,
        'end': datetime.combine(appointment.date, appointment.end_time).strftime('%Y-%m-%dT%H:%M:%S') if appointment.date and appointment.end_time else None,
        'notes': appointment.notes,
    } for appointment in patient_appointments]
    
    return render(request, 'appointments/patient_calendar.html', {'appointments': serialized_appointments})


@login_required(login_url='doctor-login')
@allowed_users(allowed_roles=['doctor'])
def doctor_calendar_view(request):
    return render(request, 'appointments/doctor_calendar.html')

@login_required(login_url='staff-login')
@allowed_users(allowed_roles=['staff'])
def staff_calendar_view(request):
    return render(request, 'appointments/staff_calendar.html')


@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def view_patient_appointments(request):
    patient = request.user.patient 
    appointments = Appointment.objects.filter(patient=patient).order_by('-date_and_time')

    context = {
        'appointments': appointments
    }
    return render(request, 'appointments/patient_appointment_list.html', context)

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def patient_view_appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    context = {
        'appointment': appointment
    }
    return render(request, 'appointments/patient_appointment_details.html', context)

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id, patient=request.user.patient)  

    if request.method == 'POST':
        slot = Slot.objects.get(start_time=appointment.start_time,
                                end_time=appointment.end_time,
                                date=appointment.date,
                                doctor=appointment.doctor)

        slot.is_available = True
        slot.patient = None
        slot.save()

        appointment.delete()

        return redirect('patient-appointment-list')
    return render(request, 'appointments/patient_appointment_delete.html', {'appointment': appointment})

