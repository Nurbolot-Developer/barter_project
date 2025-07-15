from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить безопасные методы (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Только владелец может редактировать или удалять
        return obj.user == request.user
