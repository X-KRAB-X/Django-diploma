from rest_framework.permissions import BasePermission


class OrderHistoryPermission(BasePermission):
    """
    Класс разрешений для orders.

    Служит проверкой того, что пользователь не пытается
    увидеть историю заказов анонимного профиля.
    """

    def has_permission(self, request, view):
        if request.method == 'GET' and not request.user.is_authenticated:
            return False
        else:
            return True
