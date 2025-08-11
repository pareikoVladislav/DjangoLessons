from .object_permissions import IsOwnerOrReadOnly
from .view_permissions import CanGetTopBorrower, IsWorkHour, CategoryStaffWritePermission

__all__ = [
    "CategoryStaffWritePermission",
    "IsOwnerOrReadOnly",
    "CanGetTopBorrower",
    "IsWorkHour",
]
