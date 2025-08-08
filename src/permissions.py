from django.utils import timezone
from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)


class CanGetTopBorrower(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('library.can_get_top_borrower')


class IsWorkHour(BasePermission):
    def has_permission(self, request, view):
        current = timezone.localtime().hour + 4

        print("="*100)
        print("CURRENT HOUR")
        print(current)
        print("="*100)

        return 8 <= current < 18


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.id == obj.publisher.id
