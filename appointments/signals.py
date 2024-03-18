from django.db.models.signals import post_save
from django.dispatch import receiver

from appointments.models import Appointment
from appointments.tasks import send_appointment_confirmation, send_appointment_confirmation_sms

@receiver(post_save, sender=Appointment)
def send_appointment_confirmation_message(sender, instance, created, **kwargs):
    if created:
        send_appointment_confirmation_sms(instance.id)

@receiver(post_save, sender=Appointment)
def send_appointment_confirmation_mail(sender, instance, created, **kwargs):
    if created:
        send_appointment_confirmation.delay(instance.id)


