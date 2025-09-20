from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StaffViewSet, DoctorViewSet, SpecializationViewSet

router = DefaultRouter()
router.register(r'staffs', StaffViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'specializations', SpecializationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
