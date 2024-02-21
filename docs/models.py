from django.db import models
    
class PatientPrescription(models.Model):
    patient = models.ForeignKey('users.Patient', null=True, on_delete=models.CASCADE)
    prescription = models.FileField(upload_to='patient_documents/patient_prescriptions/')
    date = models.DateTimeField(auto_now_add=True)
    
class PatientReport(models.Model):
    patient = models.ForeignKey('users.Patient', null=True, on_delete=models.CASCADE)
    report = models.FileField(upload_to='patient_documents/patient_reports/')
    date = models.DateTimeField(auto_now_add=True)
    
class PatientBills(models.Model):
    patient = models.ForeignKey('users.Patient', null=True, on_delete=models.CASCADE)
    bill = models.FileField(upload_to='patient_documents/patient_bills/')
    date = models.DateTimeField(auto_now_add=True)
    
class PatientVaccination(models.Model):
    patient = models.ForeignKey('users.Patient', null=True, on_delete=models.CASCADE)
    vaccine = models.FileField(upload_to='patient_documents/patient_vaccines/')
    date = models.DateTimeField(auto_now_add=True)
