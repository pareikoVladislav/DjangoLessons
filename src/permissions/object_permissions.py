from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        publisher = getattr(obj, 'publisher', None)
        publisher_id = getattr(publisher, 'id', None)
        return bool(request.user and request.user.is_authenticated and request.user.id == publisher_id)
