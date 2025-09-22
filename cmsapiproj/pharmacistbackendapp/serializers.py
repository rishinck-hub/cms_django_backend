from rest_framework import serializers
from .models import (
    Unitmaster, MedicineCategory, Medicine, MedicineStock,
    Bill, PrescriptionItem, BillItem
)
from doctorbackendapp.serializers import MedicinePrescriptionSerializer


class UnitmasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unitmaster
        fields = ['unitid', 'unitname']

    def validate_unitname(self, value):
        if not value.strip():
            raise serializers.ValidationError("Unit name cannot be empty.")
        return value


class MedicineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineCategory
        fields = ['medicinecategoryid', 'medicinecategoryname']

    def validate_medicinecategoryname(self, value):
        if not value.strip():
            raise serializers.ValidationError("Category name cannot be empty.")
        return value


class MedicineSerializer(serializers.ModelSerializer):
    # Write using PK, read nested object details
    unitid = serializers.PrimaryKeyRelatedField(queryset=Unitmaster.objects.all())
    medicinecategoryid = serializers.PrimaryKeyRelatedField(queryset=MedicineCategory.objects.all())
    unitid_detail = UnitmasterSerializer(source='unitid', read_only=True)
    medicinecategoryid_detail = MedicineCategorySerializer(source='medicinecategoryid', read_only=True)

    class Meta:
        model = Medicine
        fields = [
            'medicineid', 'medicinename', 'manufacturedate', 'expirydate',
            'unitquantity', 'unitid', 'unitid_detail', 'price', 'unitprice',
            'medicinecategoryid', 'medicinecategoryid_detail'
        ]

    def validate_medicinename(self, value):
        if not value.strip():
            raise serializers.ValidationError("Medicine name cannot be empty.")
        return value

    def validate(self, data):
        if ('expirydate' in data and 'manufacturedate' in data and
                data['expirydate'] <= data['manufacturedate']):
            raise serializers.ValidationError("Expiry date must be after manufacture date.")
        if 'price' in data and data['price'] <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        if 'unitprice' in data and data['unitprice'] <= 0:
            raise serializers.ValidationError("Unit price must be greater than zero.")
        return data


class MedicineStockSerializer(serializers.ModelSerializer):
    # medicineid = MedicineSerializer(read_only=True)

    # class Meta:
    #     model = MedicineStock
    #     fields = ['medicinestockid', 'stockhand', 'reorderlevel', 'purchase', 'issuance', 'medicineid', 'createddate']

    # def validate(self, data):
    #     for field in ['stockhand', 'reorderlevel', 'purchase', 'issuance']:
    #         if data.get(field, 0) < 0:
    #             raise serializers.ValidationError(f"{field} cannot be negative.")
    #     return data
    medicineid = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all())
    medicine_detail = MedicineSerializer(source='medicineid', read_only=True)

    class Meta:
        model = MedicineStock
        fields = ['medicinestockid', 'stockhand', 'reorderlevel', 'purchase', 'issuance', 'medicineid', 'medicine_detail', 'createddate']

    def validate(self, data):
        for field in ['stockhand', 'reorderlevel', 'purchase', 'issuance']:
            if data.get(field, 0) < 0:
                raise serializers.ValidationError(f"{field} cannot be negative.")
        return data


class BillSerializer(serializers.ModelSerializer):
    prescription = MedicinePrescriptionSerializer(read_only=True)
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Bill
        fields = ['id', 'prescription', 'created_at', 'created_by', 'total_amount']

    def validate_total_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Total amount cannot be negative.")
        return value


class PrescriptionItemSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(read_only=True)

    class Meta:
        model = PrescriptionItem
        fields = ['id', 'medicine', 'quantity']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value


class BillItemSerializer(serializers.ModelSerializer):
    bill = BillSerializer(read_only=True)
    prescription_item = PrescriptionItemSerializer(read_only=True)

    class Meta:
        model = BillItem
        fields = ['id', 'bill', 'prescription_item', 'total_price']

    def validate_total_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Total price cannot be negative.")
        return value

    def validate(self, data):
        # Additional validation can be added here
        return data

    def create(self, validated_data):
        bill_item = super().create(validated_data)
        bill_item.bill.update_total()
        return bill_item
