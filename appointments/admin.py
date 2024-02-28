from django.contrib import admin
from .models import Appointment, AppointmentException, Slot

admin.site.register(Appointment)
admin.site.register(AppointmentException)
admin.site.register(Slot)
