from rest_framework import serializers
from .models import Consultation, MedicinePrescription

class MedicinePrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicinePrescription
        fields = "__all__"   # or list specific fields if you want more control


class ConsultationSerializer(serializers.ModelSerializer):
    prescriptions = MedicinePrescriptionSerializer(many=True, required=False)

    class Meta:
        model = Consultation
        fields = "__all__"

    def create(self, validated_data):
        prescriptions_data = validated_data.pop("prescriptions", [])
        consultation = Consultation.objects.create(**validated_data)
        for presc in prescriptions_data:
            MedicinePrescription.objects.create(consultation=consultation, **presc)
        return consultation
