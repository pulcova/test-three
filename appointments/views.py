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

import os

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
        form = PatientAppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            appointment = form.save(commit=False)

            appointment.reason = form.cleaned_data['reason']
            appointment.notes = form.cleaned_data['notes']

            supporting_document = request.FILES.get('supporting_document')
            if supporting_document:
                original_filename = supporting_document.name
                current_date = datetime.now().strftime('%Y-%m-%d')
                new_filename = f"{appointment.patient.name}_{current_date}_{original_filename}"
                appointment.supporting_document.name = new_filename

            slot = Slot.objects.get(doctor=appointment.doctor, date=appointment.date, start_time=appointment.start_time, end_time=appointment.end_time)

            slot.is_available = False
            slot.patient = appointment.patient
            slot.save()

            appointment.save()

            # send_appointment_confirmation_email(appointment)
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
    user = request.user
    doctor = Doctor.objects.get(user=user)
    doctor_appointments = Appointment.objects.filter(doctor=doctor, date__isnull=False)
    
    serialized_appointments = [{
        'title': appointment.reason,  
        'start': datetime.combine(appointment.date, appointment.start_time).strftime('%Y-%m-%dT%H:%M:%S') if appointment.date and appointment.start_time else None,
        'end': datetime.combine(appointment.date, appointment.end_time).strftime('%Y-%m-%dT%H:%M:%S') if appointment.date and appointment.end_time else None,
        'patient': appointment.patient,
    } for appointment in doctor_appointments]
    
    return render(request, 'appointments/doctor_calendar.html', {'appointments': serialized_appointments})

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

        if appointment.supporting_document:
            os.remove(os.path.join(settings.MEDIA_ROOT, appointment.supporting_document.path))

        appointment.delete()

        return redirect('patient-appointment-list')
    return render(request, 'appointments/patient_appointment_delete.html', {'appointment': appointment})


@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def reschedule_appointment(request, appointment_id):
    old_appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            new_appointment = form.save(commit=False)

            # Copy data from old appointment to new appointment
            new_appointment.reason = old_appointment.reason
            new_appointment.notes = old_appointment.notes

            # Check for supporting document and rename if provided
            supporting_document = request.FILES.get('supporting_document')
            if supporting_document:
                original_filename = supporting_document.name
                current_date = datetime.now().strftime('%Y-%m-%d')
                new_filename = f"{new_appointment.patient.name}_{current_date}_{original_filename}"
                new_appointment.supporting_document.name = new_filename

            # Update slot availability
            old_slot = Slot.objects.get(
                doctor=old_appointment.doctor,
                date=old_appointment.date,
                start_time=old_appointment.start_time,
                end_time=old_appointment.end_time
            )
            old_slot.is_available = True
            old_slot.patient = None
            old_slot.save()

            # Get new slot
            new_slot_id = request.POST.get('new_slot')
            new_slot = Slot.objects.get(id=new_slot_id)

            # Assign new slot to new appointment
            new_appointment.date = new_slot.date
            new_appointment.start_time = new_slot.start_time
            new_appointment.end_time = new_slot.end_time
            new_appointment.doctor = new_slot.doctor

            # Save new appointment and update slot availability
            new_slot.is_available = False
            new_slot.patient = new_appointment.patient
            new_slot.save()
            new_appointment.save()

            # Delete old appointment
            old_appointment.delete()

            return redirect('patient-appointment-success')
        else:
            print("Form is invalid!")  
            print(form.errors) 
    else:
        form = PatientAppointmentForm()

    return render(request, 'appointments/reschedule_appointment.html', {'form': form, 'old_appointment': old_appointment})

@login_required(login_url='doctor-login')
def doctor_appointment_list_view(request):
    user = request.user
    doctor = Doctor.objects.get(user=user)
    appointments = Appointment.objects.filter(doctor=doctor)
    return render(request, 'users/doctor/doctor_dashboard.html', {'appointments': appointments})

@login_required(login_url='doctor-login')
def doctor_appointment_detail_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'appointments/doctor_appointment_details.html', {'appointment': appointment})
