from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Staff, Doctor, Specialization
from .serializers import StaffSerializer, DoctorSerializer, SpecializationSerializer


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    # permission_classes = [IsAuthenticated]


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    # permission_classes = [IsAuthenticated]


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('staff', 'specialization').all()
    serializer_class = DoctorSerializer
    # permission_classes = [IsAuthenticated]
