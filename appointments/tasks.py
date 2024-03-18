from celery import shared_task
from django.utils import timezone
from .models import FollowUp
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment

from django_twilio.client import twilio_client
from twilio.rest import Client

import logging

logger = logging.getLogger(__name__)


twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


@shared_task
def send_follow_up_reminders():
    today = timezone.now().date()
    follow_ups = FollowUp.objects.filter(due_date=today, notification_sent=False)
    print(f"Number of follow-ups: {follow_ups.count()}")  
    
    for follow_up in follow_ups:
        if follow_up.appointment is not None:  
            patient_email = follow_up.appointment.patient.email
            subject = "Follow-up Appointment Reminder"
            message = f"Dear {follow_up.appointment.patient.name},\n\nThis is a reminder for your follow-up appointment scheduled. Please ensure you are available.\n\nRegards,\nThe Clinic"

            send_mail(subject, message, settings.EMAIL_HOST_USER, [patient_email])
            
            follow_up.notification_sent = True
            follow_up.save()
        else:
            print(f"FollowUp object with id {follow_up.id} has no associated Appointment.")

@shared_task
def reset_notification_sent_flag():
    follow_ups = FollowUp.objects.filter(notification_sent=True) 
    follow_ups.update(notification_sent=False)

@shared_task
def send_appointment_confirmation_sms(appointment_id):
    instance = Appointment.objects.get(id=appointment_id)

    message = f"Dear {instance.patient.name},\n\nThis is to confirm your appointment with {instance.doctor.name} on {instance.date} at {instance.start_time}. Please acknowledge this SMS.\n\nRegards,\nThe Clinic"
    
    try:
        twilio_client.messages.create(
            body=message,
            from_=settings.TWILIO_FROM_NUMBER,
            to=[instance.patient.phone]
        )
    except Exception as e:
        logger.error(f"Error sending SMS to {instance.patient.phone}: {e}")

@shared_task
def send_appointment_confirmation(appointment_id):
    instance = Appointment.objects.get(id=appointment_id)
    
    message = f"Dear {instance.patient.name},\n\nThis is to confirm your appointment with {instance.doctor.name} on {instance.date} at {instance.start_time}. Please acknowledge this email.\n\nRegards,\nThe Clinic"
    subject = "Appointment Confirmation"

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.patient.email])
    except Exception as e:
        logger.error(f"Error sending email to {instance.patient.email}: {e}")


