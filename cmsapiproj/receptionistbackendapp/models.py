from django.db import models
from django.core.exceptions import ValidationError
from adminbackendapp.models import Doctor



# Create your models here.

class Patient(models.Model):
    BLOODGROUP_CHOICES = [
        ("A+", "A+"), ("A-", "A-"), ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"), ("O+", "O+"), ("O-", "O-")
    ]
    GENDER_CHOICES = [
        ("male", "Male"), ("female", "Female"), ("other", "Other")
    ]
    patientid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    bloodgroup = models.CharField(max_length=10, choices=BLOODGROUP_CHOICES)
    mobileno = models.CharField(max_length=20)
    address = models.TextField()
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ]
    appointmentid = models.AutoField(primary_key=True)
    appointmentdate = models.DateField()
    tokenno = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    patientid = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctorid = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        if hasattr(self, 'patient') and self.patient:
            return f"Appointment {self.tokenno} for {self.patient.name}"
        return f"Appointment {self.tokenno}"


class Billing(models.Model):
    billingid = models.AutoField(primary_key=True)
    appointmentid = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    appointmentdate = models.DateField()
    patientid = models.ForeignKey(Patient, on_delete=models.CASCADE)
    consultationfee = models.IntegerField()

    def __str__(self):
        return f"Billing {self.billingid} for Appointment {self.appointmentid_id}"
