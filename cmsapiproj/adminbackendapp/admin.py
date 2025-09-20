from django.contrib import admin
from .models import Staff, Doctor, Specialization


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'staff_name', 'gender', 'mobile_no', 'dob', 'username','password','role')
    search_fields = ('staff_name', 'mobile_no','staff_id')

    def user_role(self, obj):
        return obj.user.role if obj.user else "N/A"


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('specialization_id', 'specialization_name',)
    search_fields = ('specialization_name',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'staff', 'specialization', 'experience', 'consultation_fee', 'is_active')
    list_filter = ('is_active', 'specialization')
    search_fields = ('staff__staff_name',)


