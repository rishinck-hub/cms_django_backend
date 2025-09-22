from django.shortcuts import render
from rest_framework import viewsets
from .models import Patient, Appointment, Billing
from .serializers import PatientSerializer, AppointmentSerializer, BillingSerializer
from authentication.permissions import IsReceptionist

# Create your views here.

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsReceptionist]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsReceptionist]

class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    permission_classes = [IsReceptionist]
