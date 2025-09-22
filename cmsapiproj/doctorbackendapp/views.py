from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Consultation, MedicinePrescription
from .serializers import ConsultationSerializer, MedicinePrescriptionSerializer
from authentication.permissions import IsDoctor

# ---- Consultation Views ----
class ConsultationListCreateView(generics.ListCreateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsDoctor]


class ConsultationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsDoctor]


# ---- Medicine Prescription Views ----
class MedicinePrescriptionListCreateView(generics.ListCreateAPIView):
    queryset = MedicinePrescription.objects.all()
    serializer_class = MedicinePrescriptionSerializer
    permission_classes = [IsDoctor]


class MedicinePrescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicinePrescription.objects.all()
    serializer_class = MedicinePrescriptionSerializer
    permission_classes = [IsDoctor]
