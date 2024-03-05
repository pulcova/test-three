from django.contrib import admin
from .models import Appointment, AppointmentException, FollowUp, Slot

admin.site.register(Appointment)
admin.site.register(AppointmentException)
admin.site.register(FollowUp)
admin.site.register(Slot)
