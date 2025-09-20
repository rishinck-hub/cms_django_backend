from rest_framework import serializers
from .models import Staff, Doctor, Specialization
from datetime import date


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

    def validate_mobile_no(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Mobile number must be at least 10 digits.")
        return value

    def validate_dob(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("Staff must be at least 18 years old.")
        return value


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

    def validate_specialization_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Specialization name must be at least 3 characters.")
        return value


class DoctorSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source="staff.staff_name", read_only=True)

    class Meta:
        model = Doctor
        fields = ['doctor_id', 'staff', 'staff_name', 'specialization', 'experience', 'consultation_fee', 'is_active']

    def validate(self, data):
        staff = data.get("staff")
        if staff and staff.dob:
            today = date.today()
            age = today.year - staff.dob.year - ((today.month, today.day) < (staff.dob.month, staff.dob.day))
            if age < 25:
                raise serializers.ValidationError({"staff": "Doctor must be at least 25 years old."})
        return data

    def validate_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("Experience must be a positive number.")
        return value

    def validate_consultation_fee(self, value):
        if value <= 0:
            raise serializers.ValidationError("Consultation fee must be greater than 0.")
        return value
    def validate_staff(self, staff):
        if staff.role != "DOCTOR":
            raise serializers.ValidationError("Selected staff must have role 'DOCTOR'.")
        return staff