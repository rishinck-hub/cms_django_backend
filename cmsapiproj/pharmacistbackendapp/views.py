from rest_framework import viewsets
from .models import (
    Unitmaster, MedicineCategory, Medicine, MedicineStock,
    Bill, PrescriptionItem, BillItem
)
from .serializers import (
    UnitmasterSerializer, MedicineCategorySerializer, MedicineSerializer, MedicineStockSerializer,
    BillSerializer, PrescriptionItemSerializer, BillItemSerializer
)
from authentication.permissions import IsPharmacist

class UnitmasterViewSet(viewsets.ModelViewSet):
    queryset = Unitmaster.objects.all()
    serializer_class = UnitmasterSerializer
    permission_classes = [IsPharmacist]

class MedicineCategoryViewSet(viewsets.ModelViewSet):
    queryset = MedicineCategory.objects.all()
    serializer_class = MedicineCategorySerializer
    permission_classes = [IsPharmacist]

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsPharmacist]

class MedicineStockViewSet(viewsets.ModelViewSet):
    queryset = MedicineStock.objects.all()
    serializer_class = MedicineStockSerializer
    permission_classes = [IsPharmacist]

class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsPharmacist]

class PrescriptionItemViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer
    permission_classes = [IsPharmacist]

class BillItemViewSet(viewsets.ModelViewSet):
    queryset = BillItem.objects.all()
    serializer_class = BillItemSerializer
    permission_classes = [IsPharmacist]
