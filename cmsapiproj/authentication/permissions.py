from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    allowed_groups = ['ADMIN','RECEPTIONIST','DOCTOR','PHARMACIST']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=self.allowed_groups).exists()

        return request.user.groups.filter(name='ADMIN').exists()
    

class IsReceptionist(permissions.BasePermission):
    allowed_groups = ['ADMIN','RECEPTIONIST','DOCTOR','PHARMACIST']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=self.allowed_groups).exists()

        return request.user.groups.filter(name=['ADMIN','RECEPTIONIST']).exists()
    

class IsDoctor(permissions.BasePermission):
    allowed_groups = ['ADMIN','RECEPTIONIST','DOCTOR','PHARMACIST']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=self.allowed_groups).exists()

        return request.user.groups.filter(name=['ADMIN','DOCTOR']).exists()
    
class IsPharmacist(permissions.BasePermission):
    allowed_groups = ['ADMIN','RECEPTIONIST','DOCTOR','PHARMACIST']

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=self.allowed_groups).exists()

        return request.user.groups.filter(name=['ADMIN','PHARMACIST']).exists()
    