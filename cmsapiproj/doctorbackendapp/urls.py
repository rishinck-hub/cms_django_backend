from django.urls import path
from .views import (
    ConsultationListCreateView,
    ConsultationDetailView,
    MedicinePrescriptionListCreateView,
    MedicinePrescriptionDetailView,
)

urlpatterns = [
    path("consultations/", ConsultationListCreateView.as_view(), name="consultation-list-create"),
    path("consultations/<int:pk>/", ConsultationDetailView.as_view(), name="consultation-detail"),
    path("prescriptions/", MedicinePrescriptionListCreateView.as_view(), name="prescription-list-create"),
    path("prescriptions/<int:pk>/", MedicinePrescriptionDetailView.as_view(), name="prescription-detail"),
]
