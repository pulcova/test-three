from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Query, QueryTicket
from .utils import generate_ticket_number  
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Query)
def create_ticket(sender, instance, created, **kwargs):
    if created:  
        ticket = QueryTicket.objects.create(
            query=instance,
            ticket_number=generate_ticket_number()
        )

        send_mail(
            subject=f'Your Query Ticket #{ticket.ticket_number}',
            message=f'Your query has been registered with ticket number {ticket.ticket_number}.',
            from_email=settings.EMAIL_HOST_USER,  
            recipient_list=[instance.patient.email],  
        )
