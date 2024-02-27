from django.db import models
from django.contrib.auth.models import User
from users.models import Patient, Doctor, Staff

class Query(models.Model):
    CHANNEL_CHOICES = (
        ('WEB', 'Website'),
        ('CHAT', 'Chatbot'),
        ('SOCIAL', 'Social Media'),
        ('CALL', 'Direct Call'),
        ('IVR', 'IVR'),
    )
    CATEGORY_CHOICES = (
        ('APPT', 'Appointment'),
        ('MED', 'Medical'),
        ('BILL', 'Billing'),
        ('OTHER', 'Other'),
    )
    PRIORITY_CHOICES = (
        ('HIGH', 'High'),
        ('MED', 'Medium'),
        ('LOW', 'Low'),
    )
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('PROG', 'In-Progress'),
        ('RES', 'Resolved'),
        ('CLOSED', 'Closed'),
    )
    COLOR_CHOICES = (
        ('A', 'Red'),
        ('B', 'Green'),
        ('C', 'Blue'),
    )
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    text = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    color_code = models.CharField(max_length=1, choices=COLOR_CHOICES, default='A')
    assigned_staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)   
    source_details = models.CharField(max_length=50, null=True, blank=True)
    ivr_option = models.CharField(max_length=50, null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    resolution_time = models.DateTimeField(null=True, blank=True)
    follow_up_required = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
