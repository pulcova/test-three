from django.db import models
from users.models import Patient, Doctor, Staff

class MedicationCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name  # Example: "Topical"

class Medication(models.Model):
    name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255)
    dosage_forms = models.CharField(max_length=255)  # Example: "Cream, Ointment"
    dosage_strength = models.CharField(max_length=255)  # Example: "0.1%, 10mg"
    category = models.ForeignKey(MedicationCategory, on_delete=models.PROTECT)
    side_effects = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.brand_name} ({self.generic_name}) - {self.dosage_strength}"

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT) 
    date = models.DateTimeField()
    doctors_notes = models.TextField(blank=True)  
    staff_instructions = models.TextField(blank=True) 

    def __str__(self):
        return f"Consultation for {self.patient} on {self.date.strftime('%Y-%m-%d')}"

class Prescription(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)  
    dosage_quantity = models.CharField(max_length=50)  
    dosage_unit = models.CharField(max_length=50) 
    frequency = models.CharField(max_length=255)  # Example: "Twice Daily" 
    refills = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    instructions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=(('ACTIVE', 'Active'), ('DISCONTINUED', 'Discontinued')), default='ACTIVE')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medication} - {self.dosage_quantity} {self.dosage_unit} {self.frequency}"

class TreatmentPlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    prescriptions = models.ManyToManyField(Prescription, blank=True)  

    def __str__(self):
        return f"{self.patient} - {self.name}"

class PhototherapySession(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment_plan = models.ForeignKey(TreatmentPlan, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField()
    dosage = models.CharField(max_length=50)  # Example: "30 Joules/cm2"
    device_type = models.CharField(max_length=100, blank=True) # Example: "Narrowband UVB"
    area_treated = models.CharField(max_length=255, blank=True)  # Example: "Face, Hands"
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True) 

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} - {self.device_type} ({self.dosage})"



