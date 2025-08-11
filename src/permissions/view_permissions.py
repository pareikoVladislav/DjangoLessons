from django.utils import timezone
from rest_framework.permissions import BasePermission, SAFE_METHODS

class CanGetTopBorrower(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('library.can_get_top_borrower')


class IsWorkHour(BasePermission):
    def has_permission(self, request, view):
        current = timezone.localtime().hour
        return 8 <= current < 18

class CategoryStaffWritePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and user.is_staff)
