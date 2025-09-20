from django.db import models


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    staff_name = models.CharField(max_length=100, unique=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
    )
    mobile_no = models.CharField(max_length=15, unique=True)
    dob = models.DateField()
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  
    role = models.CharField(
        max_length=20,
        choices=[
            ('ADMIN', 'Admin'),
            ('RECEPTIONIST', 'Receptionist'),
            ('DOCTOR', 'Doctor'),
            ('PHARMACIST', 'Pharmacist'),
        ],
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.staff_name} - {self.role}'


class Specialization(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    specialization_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.specialization_name


class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE) 
    specialization = models.ForeignKey(
        Specialization, on_delete=models.SET_NULL, null=True, blank=True
    )
    experience = models.PositiveIntegerField(help_text="Experience in years")
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.staff.staff_name} - {self.specialization}'


