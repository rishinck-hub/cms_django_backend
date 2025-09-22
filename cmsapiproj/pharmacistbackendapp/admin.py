from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Unitmaster, MedicineCategory, Medicine, MedicineStock,
     Bill, PrescriptionItem, BillItem
)

admin.site.register(Unitmaster)
admin.site.register(MedicineCategory)
admin.site.register(Medicine)
admin.site.register(MedicineStock)
# admin.site.register(Prescription)
# admin.site.register(PrescriptionDetail)
admin.site.register(Bill)
admin.site.register(PrescriptionItem)
admin.site.register(BillItem)
