from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Staff, Specialization, Doctor
import datetime


class StaffAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff1 = Staff.objects.create(
            staff_name="Alice",
            username="alice",
            password="testpass123",
            gender="Female",
            mobile_no="1234567890",
            dob="1990-01-01",
            role="RECEPTIONIST",
            is_active=True,
        )

    def test_list_staff(self):
        url = reverse("staff-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_search_staff_by_name(self):
        url = reverse("staff-list")
        response = self.client.get(url, {"staff_name": "Alice"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_staff(self):
        url = reverse("staff-list")
        data = {
            "staff_name": "Bob",
            "username": "bob",
            "password": "testpass123",
            "gender": "Male",
            "mobile_no": "9876543210",
            "dob": "1992-05-15",
            "role": "DOCTOR",
            "is_active": True,
        }
        response = self.client.post(url, data, format="json")
        print("Create staff response:", response.data)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SpecializationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.spec1 = Specialization.objects.create(
            specialization_name="Cardiology"
        )

    def test_list_specializations(self):
        url = reverse("specialization-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_specialization(self):
        url = reverse("specialization-list")
        data = {"specialization_name": "Neurology"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from .models import Staff, Doctor, Specialization

class DoctorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Valid doctor staff
        self.staff = Staff.objects.create(
            staff_name="Dr. Smith",
            username="drsmith",
            password="testpass123",
            gender="Male",
            mobile_no="1112223333",
            dob="1985-07-20",
            role="DOCTOR",
            is_active=True,
        )

        # Specialization
        self.spec1 = Specialization.objects.create(
            specialization_name="Orthopedics"
        )

        # Existing doctor
        self.doctor = Doctor.objects.create(
            staff=self.staff,
            specialization=self.spec1,
            experience=10,
            consultation_fee=500.00,
            is_active=True,
        )

    def test_list_doctors(self):
        url = reverse("doctor-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_doctor(self):
        new_staff = Staff.objects.create(
            staff_name="Dr. John",
            username="drjohn",
            password="testpass123",
            gender="Male",
            mobile_no="4445556666",
            dob="1990-03-15",
            role="DOCTOR",
            is_active=True,
        )
        url = reverse("doctor-list")
        data = {
            "staff": new_staff.staff_id,
            "specialization": self.spec1.specialization_id,
            "experience": 5,
            "consultation_fee": "300.00",
            "is_active": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_doctor_with_non_doctor_staff_should_fail(self):
        # Create a staff with wrong role
        invalid_staff = Staff.objects.create(
            staff_name="Receptionist User",
            username="recept1",
            password="testpass123",
            gender="Female",
            mobile_no="9998887777",
            dob="1995-05-05",
            role="RECEPTIONIST",   # ❌ Not a doctor
            is_active=True,
        )
        url = reverse("doctor-list")
        data = {
            "staff": invalid_staff.staff_id,
            "specialization": self.spec1.specialization_id,
            "experience": 2,
            "consultation_fee": "200.00",
            "is_active": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Correct way to check the error
        self.assertIn("Selected staff must have role 'DOCTOR'.", str(response.data['staff'][0]))


    def test_search_doctor_by_specialization(self):
        url = reverse("doctor-list")
        response = self.client.get(url, {"specialization": self.spec1.specialization_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
