from celery import shared_task
from django.utils import timezone
from .models import FollowUp
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_follow_up_reminders():
    print("Task started")
    today = timezone.now().date()
    follow_ups = FollowUp.objects.filter(due_date=today, notification_sent=False)
    print(f"Number of follow-ups: {follow_ups.count()}")  # New print statement
    
    for follow_up in follow_ups:
        if follow_up.appointment is not None:  # Check if appointment is not None
            patient_email = follow_up.appointment.patient.email
            subject = "Follow-up Appointment Reminder"
            message = f"Dear {follow_up.appointment.patient.name},\n\nThis is a reminder for your follow-up appointment scheduled. Please ensure you are available.\n\nRegards,\nThe Clinic"
            
            # Print out the content and recipient's email address for debugging
            print("Email Content:")
            print(f"Subject: {subject}")
            print(f"Message: {message}")
            print(f"To: {patient_email}")

            send_mail(subject, message, settings.EMAIL_HOST_USER, [patient_email])
            
            follow_up.notification_sent = True
            follow_up.save()
            
            # follow_ups_next_day = FollowUp.objects.filter(due_date=today + timezone.timedelta(days=1), appointment=follow_up.appointment)
            # for follow_up_next_day in follow_ups_next_day:
            #     follow_up_next_day.notification_sent = False
            #     follow_up_next_day.save()
        else:
            print(f"FollowUp object with id {follow_up.id} has no associated Appointment.")

@shared_task
def reset_notification_sent_flag():
    print("Resetting notification_sent flag")
    # Find all FollowUp objects where notification_sent is True
    follow_ups = FollowUp.objects.filter(notification_sent=True)
    
    # Update notification_sent flag to False for all found FollowUp objects
    follow_ups.update(notification_sent=False)