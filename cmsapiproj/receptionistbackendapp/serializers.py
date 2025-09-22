from rest_framework import serializers
from .models import Patient, Appointment, Billing

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value

    def validate_bloodgroup(self, value):
        valid_bloodgroups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        if value not in valid_bloodgroups:
            raise serializers.ValidationError("Invalid blood group.")
        return value

    def validate_gender(self, value):
        if value.lower() not in ["male", "female", "other"]:
            raise serializers.ValidationError("Gender must be 'male', 'female', or 'other'.")
        return value

    def validate_mobileno(self, value):
        if not (value.isdigit() and len(value) == 10 and value[0] in "6789"):
            raise serializers.ValidationError("Mobile number must start with 6, 7, 8, or 9 and be 10 digits.")
        return value

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate_date(self, value):
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("Appointment date must be today or in the future.")
        return value

    def validate_status(self, value):
        valid_status = ["pending", "confirmed", "completed", "cancelled"]
        if value not in valid_status:
            raise serializers.ValidationError("Status must be one of: pending, confirmed, completed, cancelled.")
        return value

class BillingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patientid.name', read_only=True)
    appointment_token = serializers.IntegerField(source='appointmentid.tokenno', read_only=True)
    appointmentdate = serializers.DateField()
    consultationfee = serializers.IntegerField()
    
    class Meta:
        model = Billing
        fields = '__all__'
    
    
    def validate_appointmentid(self, value):
        """Validate appointment ID"""
        if value is None:
            raise serializers.ValidationError("Appointment ID is required.")
        
        # Check if appointment exists
        if not Appointment.objects.filter(appointmentid=value.appointmentid).exists():
            raise serializers.ValidationError("Invalid appointment ID. Appointment does not exist.")
        
        # Check if appointment is confirmed or completed (only these can be billed)
        if value.status not in ['confirmed', 'completed']:
            raise serializers.ValidationError("Only confirmed or completed appointments can be billed.")
        
        return value
    
    def validate_patientid(self, value):
        """Validate patient ID"""
        if value is None:
            raise serializers.ValidationError("Patient ID is required.")
        
        # Check if patient exists
        if not Patient.objects.filter(patientid=value.patientid).exists():
            raise serializers.ValidationError("Invalid patient ID. Patient does not exist.")
        
        # Check if patient is active
        if not value.isactive:
            raise serializers.ValidationError("Cannot create billing for inactive patient.")
        
        return value
    
    def validate(self, data):
        """Cross-field validation"""
        # Check if appointment belongs to the specified patient
        appointment = data.get('appointmentid')
        patient = data.get('patientid')
        
        if appointment and patient:
            if appointment.patientid != patient:
                raise serializers.ValidationError(
                    "The appointment does not belong to the specified patient."
                )
        
        # Only set appointment date from the appointment if not provided
        if appointment and 'appointmentdate' not in data:
            data['appointmentdate'] = appointment.appointmentdate
        
        # Only set consultation fee from the appointment if not provided
        if appointment and 'consultationfee' not in data:
            data['consultationfee'] = appointment.consultationfee
        
        # Check for duplicate billing for the same appointment (only for new instances)
        appointment_id = data.get('appointmentid')
        if appointment_id and self.instance is None:  # Only for new instances
            existing_billing = Billing.objects.filter(appointmentid=appointment_id).first()
            if existing_billing:
                # Instead of creating new, update existing
                self.instance = existing_billing
        
        return data
    
    def create(self, validated_data):
        """Create or update billing record - allows upsert behavior"""
        appointment_id = validated_data.get('appointmentid')
        
        # Check if billing already exists for this appointment
        existing_billing = Billing.objects.filter(appointmentid=appointment_id).first()
        
        if existing_billing:
            # Update existing billing record
            for attr, value in validated_data.items():
                setattr(existing_billing, attr, value)
            existing_billing.save()
            return existing_billing
        else:
            # Create new billing record
            return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Update existing billing record"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance