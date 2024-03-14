from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Query, QueryTicket
from .utils import generate_ticket_number
from .tasks import send_query_creation_notification, send_query_resolution_notification, send_staff_assignment_notification

@receiver(post_save, sender=Query)
def create_ticket_and_send_notifications(sender, instance, created, **kwargs):
    if created:  
        ticket = QueryTicket.objects.create(
            query=instance,
            ticket_number=generate_ticket_number()
        )
        send_query_creation_notification.delay(instance.id)

@receiver(post_save, sender=Query)
def send_resolution_notification(sender, instance, created, **kwargs):
    send_query_resolution_notification.delay(instance.id)

@receiver(m2m_changed, sender=Query.assigned_staff.through)
def send_staff_notifications(sender, instance, action, **kwargs):
    if action == 'post_add': 
       send_staff_assignment_notification.delay(instance.id) 
