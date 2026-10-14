from rest_framework.permissions import BasePermission, SAFE_METHODS

def is_manager(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name="Manager").exists())

def is_delivery(user):
    return user.is_authenticated and user.groups.filter(name="Delivery crew").exists()

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff) or request.method in SAFE_METHODS

class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return is_manager(request.user)

class IsManagerAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return is_manager(request.user)

class IsDeliveryOrManager(BasePermission):
    def has_permission(self, request, view):
        return is_manager(request.user) or is_delivery(request.user)
