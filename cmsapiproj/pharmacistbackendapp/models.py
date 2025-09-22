
from django.db import models
from django.contrib.auth.models import User
# from doctorbackendapp.models import MedicinePrescription
  # Importing from the same app to avoid circular dependency


class Unitmaster(models.Model):
    unitid = models.AutoField(primary_key=True)
    unitname = models.CharField(max_length=100)

    def __str__(self):
        return self.unitname


class MedicineCategory(models.Model):
    medicinecategoryid = models.AutoField(primary_key=True)
    medicinecategoryname = models.CharField(max_length=100)

    def __str__(self):
        return self.medicinecategoryname


class Medicine(models.Model):
    medicineid = models.AutoField(primary_key=True)
    medicinename = models.CharField(max_length=200)
    manufacturedate = models.DateField()
    expirydate = models.DateField()
    unitquantity = models.CharField(max_length=100)
    unitid = models.ForeignKey(Unitmaster, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unitprice = models.DecimalField(max_digits=10, decimal_places=2)
    medicinecategoryid = models.ForeignKey(MedicineCategory, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.medicinename


class MedicineStock(models.Model):
    medicinestockid = models.AutoField(primary_key=True)
    stockhand = models.IntegerField()
    reorderlevel = models.IntegerField()
    purchase = models.IntegerField()
    issuance = models.IntegerField()
    medicineid = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    createddate = models.DateTimeField()

    def __str__(self):
        return f"Stock for {self.medicineid.medicinename} (ID: {self.medicinestockid})"


# class Prescription(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     notes = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"Prescription #{self.id}"


# class PrescriptionDetail(models.Model):
#     medicineprescriptionid = models.AutoField(primary_key=True)
#     prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="prescription_details")
#     medicineid = models.ForeignKey(Medicine, on_delete=models.CASCADE)
#     dosage = models.CharField(max_length=100, null=True, blank=True)
#     frequency = models.CharField(max_length=100, null=True, blank=True)
#     duration = models.CharField(max_length=100, null=True, blank=True)
#     quantity = models.IntegerField(null=True, blank=True)
#     appointmentid = models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return f"Prescription Detail {self.medicineprescriptionid}"


class Bill(models.Model):
    prescription = models.OneToOneField("doctorbackendapp.MedicinePrescription", on_delete=models.CASCADE, related_name="bill")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total(self):
        # Update the total by summing up the prices from BillItems
        self.total_amount = sum(item.total_price for item in self.items.all())
        self.save()


class PrescriptionItem(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.medicine.medicinename} x {self.quantity}"


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="items")
    prescription_item = models.OneToOneField(PrescriptionItem, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        medicine = self.prescription_item.medicine
        qty = self.prescription_item.quantity
        # Update stock if enough stock exists
        stock = MedicineStock.objects.filter(medicineid=medicine).order_by('-createddate').first()

        if stock and stock.stockhand >= qty:
            stock.stockhand -= qty
            stock.save()
        elif stock:
            raise ValueError(f"Not enough stock for {medicine.medicinename}")
        else:
            raise ValueError(f"Stock not found for {medicine.medicinename}")

        # Calculate total price
        self.total_price = medicine.price * qty
        super().save(*args, **kwargs)

        # Update the bill's total amount
        self.bill.update_total()

    def __str__(self):
        return f"Bill Item: {self.prescription_item.medicine.medicinename} for {self.bill}"
