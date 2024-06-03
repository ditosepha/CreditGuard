from rest_framework.permissions import BasePermission, SAFE_METHODS

class CustomPermission(BasePermission):
    # allows users to only send SAFE and POST methods.
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == 'POST':
            return True
        else:
            return False