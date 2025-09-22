from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Staff, Doctor, Specialization
from .serializers import StaffSerializer, DoctorSerializer, SpecializationSerializer
# from authapp.permissions import IsAdmin, IsDoctor
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsAdminOrReadOnly

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAdminOrReadOnly]


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAdminOrReadOnly]



class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('staff', 'specialization').all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdminOrReadOnly]

