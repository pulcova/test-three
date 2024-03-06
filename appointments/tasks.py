from celery import shared_task
from django.utils import timezone
from .models import FollowUp
from django.core.mail import send_mail
from django.conf import settings

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