from celery import shared_task
from django.core.mail import send_mail
from django_twilio.client import twilio_client
from twilio.rest import Client

from .models import Query
from django.conf import settings

twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_notification(instance, subject, message):
    try:
        send_mail(
            subject, 
            message, 
            from_email=settings.EMAIL_HOST_USER, 
            recipient_list=[instance.patient.email],
        ) 

        twilio_client.messages.create(
            body=message,
            from_=settings.TWILIO_FROM_NUMBER,  
            to=[instance.patient.phone]
        )
        print("Notifications sent successfully")  
    except Exception as e:
        print(f"Failed to send notifications: {e}") 
        
@shared_task
def send_query_creation_notification(query_id):
    instance = Query.objects.get(id=query_id)
    message = f'Your query has been registered with ticket number {instance.queryticket.ticket_number}.'
    subject = f'Your Query Ticket #{instance.queryticket.ticket_number}'
    send_notification(instance, subject, message) 

@shared_task
def send_query_resolution_notification(query_id):
    instance = Query.objects.get(id=query_id)
    if instance.status == 'RES':  
        message = f'Dear {instance.patient.name},\n\nYour query ({instance.text}) has been resolved. Please log in to view the resolution details.\n\nBest Regards,\nSupport Team'
        subject = 'Your Query Has Been Resolved'
        send_notification(instance, subject, message)

@shared_task
def send_staff_assignment_notification(query_id):
    instance = Query.objects.get(id=query_id)
    for staff in instance.assigned_staff.all():
        subject = f'New Query Assigned: Ticket #{instance.queryticket.ticket_number}' 
        message = (f'A new query has been assigned to you. '
                   f'Ticket Number: {instance.queryticket.ticket_number}\n'
                   f'Please access the system to view and address the query.')
        send_mail(subject, message, settings.EMAIL_HOST_USER, [staff.email]) 
