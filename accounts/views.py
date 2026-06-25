from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Status
from .serializers import StatusSerializer, UserSerializer, UserWriteSerializer

User = get_user_model()


class IsStaffOrSelf(permissions.BasePermission):
    """
    Staff can do anything. A regular user may only read/edit their own
    User record -- prevents students from editing each other via the API.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        # Anyone logged in can view statuses; only staff can create/edit/delete
        # the tag list itself.
        if self.action in ("list", "retrieve"):
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().prefetch_related("statuses")
    permission_classes = [permissions.IsAuthenticated, IsStaffOrSelf]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return UserWriteSerializer
        return UserSerializer

    def get_queryset(self):
        # Non-staff users only ever see themselves in list/detail results.
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(pk=self.request.user.pk)

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
