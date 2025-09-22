from django.db import models
from receptionistbackendapp.models import Appointment
# from pharmacistbackendapp.models import Medicine

# Create your models here.

class Consultation(models.Model):
    consultationid = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)  
    symptoms = models.TextField()
    diagnosis = models.TextField()
    notes = models.TextField(blank=True, null=True)
    createddate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation {self.consultationid} - Appointment {self.appointment_id}"

    
class MedicinePrescription(models.Model):
    medicineprescriptionid = models.AutoField(primary_key=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name="prescriptions")
    medicine = models.ForeignKey("pharmacistbackendapp.Medicine", on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)

    def __str__(self):
        return f"Prescription {self.medicineprescriptionid} for Appointment {self.appointment_id}"