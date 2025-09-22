from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UnitmasterViewSet, MedicineCategoryViewSet, MedicineViewSet, MedicineStockViewSet,
    BillViewSet, PrescriptionItemViewSet, BillItemViewSet
)

router = DefaultRouter()
#router.register(r'units', UnitmasterViewSet)

router.register(r'units', UnitmasterViewSet, basename='unitmaster')

router.register(r'medicinecategories', MedicineCategoryViewSet)
router.register(r'medicines', MedicineViewSet)
router.register(r'medicinestocks', MedicineStockViewSet)
router.register(r'bills', BillViewSet)
router.register(r'prescriptionitems', PrescriptionItemViewSet)
router.register(r'billitems', BillItemViewSet)

# urlpatterns = [
#     path('api/', include(router.urls)),
# ]
urlpatterns = [
    path('', include(router.urls)),
]