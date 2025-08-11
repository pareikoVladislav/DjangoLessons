from django.utils import timezone
from rest_framework.permissions import (
    BasePermission,
)

class CanGetTopBorrower(BasePermission):
    def has_permission(self, request, view):
        print("="*50)
        print(request.user)
        print("="*50)

        return request.user.has_perm('library.can_get_top_borrower')


class IsWorkHour(BasePermission):
    def has_permission(self, request, view):
        current = timezone.localtime().hour + 4
        return 8 <= current < 18