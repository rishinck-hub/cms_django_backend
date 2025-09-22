from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Staff, Specialization, Doctor
from datetime import date


class StaffModelTest(TestCase):
    def setUp(self):
        self.staff = Staff.objects.create(
            staff_name="John Doe",
            gender="Male",
            mobile_no="1234567890",
            email="johndoe@example.com",
            address="123 Street, City",
            dob=date(1990, 1, 1),
            role="DOCTOR",
        )

    def test_staff_creation(self):
        self.assertEqual(self.staff.staff_name, "John Doe")
        self.assertEqual(self.staff.role, "DOCTOR")
        self.assertTrue(self.staff.is_active)

    def test_staff_string_representation(self):
        self.assertEqual(str(self.staff), "John Doe - DOCTOR")


class SpecializationModelTest(TestCase):
    def setUp(self):
        self.specialization = Specialization.objects.create(
            specialization_name="Cardiology"
        )

    def test_specialization_creation(self):
        self.assertEqual(self.specialization.specialization_name, "Cardiology")

    def test_specialization_string_representation(self):
        self.assertEqual(str(self.specialization), "Cardiology")


class DoctorModelTest(TestCase):
    def setUp(self):
        self.staff_doctor = Staff.objects.create(
            staff_name="Dr. Smith",
            gender="Male",
            mobile_no="9876543210",
            email="drsmith@example.com",
            address="456 Avenue, City",
            dob=date(1985, 5, 15),
            role="DOCTOR",
        )
        self.specialization = Specialization.objects.create(
            specialization_name="Dermatology"
        )

    def test_doctor_creation_valid(self):
        doctor = Doctor.objects.create(
            staff=self.staff_doctor,
            specialization=self.specialization,
            experience=10,
            consultation_fee=500.00,
        )
        self.assertEqual(doctor.staff.staff_name, "Dr. Smith")
        self.assertEqual(doctor.specialization.specialization_name, "Dermatology")

    def test_doctor_invalid_role(self):
        staff_non_doctor = Staff.objects.create(
            staff_name="Receptionist 1",
            gender="Female",
            mobile_no="1112223333",
            email="receptionist@example.com",
            address="789 Street, City",
            dob=date(1992, 7, 10),
            role="RECEPTIONIST",
        )

        doctor = Doctor(
            staff=staff_non_doctor,
            specialization=self.specialization,
            experience=5,
            consultation_fee=300.00,
        )
        with self.assertRaises(ValidationError):
            doctor.full_clean()  # should raise ValidationError

    def test_doctor_string_representation(self):
        doctor = Doctor.objects.create(
            staff=self.staff_doctor,
            specialization=self.specialization,
            experience=7,
            consultation_fee=400.00,
        )
        self.assertEqual(str(doctor), "Dr. Smith - Dermatology")
