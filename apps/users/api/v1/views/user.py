from rest_framework import parsers, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.api.v1.serializers.user import ChangeUserActiveSerializer, DetailUserSerializer, ListUserSerializer
from apps.users.api.v1.serializers.user_profile import UserProfileUploadPhotoSerializer
from apps.users.filters import UserFilter
from apps.users.models import User
from apps.users.permissions import IsAdminPermissions
from apps.users.services.user_profile import UserProfileService
from apps.users.tasks.users_send_email import send_email_about_reset_password
from mixins.views_mixin import ListSerializerClassMixin


class UserViewSet(ListSerializerClassMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAdminPermissions)
    queryset = User.objects.select_related('userprofile')
    list_serializer_class = ListUserSerializer
    serializer_class = DetailUserSerializer
    filterset_class = UserFilter

    def get_queryset(self):
        user = self.request.user
        match user.type_user:
            case User.TypeUserChoices.ADMIN.value:
                return self.queryset.all()
            case _:
                return self.queryset.none()

    @action(
        methods=['POST'],
        detail=True,
        parser_classes=(parsers.FormParser, parsers.MultiPartParser),
        serializer_class=UserProfileUploadPhotoSerializer,
    )
    def upload_photo(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = self.get_object()
        UserProfileService.upload_user_photo(request, user_obj.userprofile)
        return Response({'status': 'success'})

    @action(
        detail=True,
        methods=['get'],
    )
    def password_reset(self, request, *args, **kwargs):
        user = self.get_object()
        password = User.objects.make_random_password(8)
        user.set_password(password)
        user.save(update_fields=['password'])
        userprofile = user.userprofile
        userprofile.should_change_password = True
        userprofile.save(update_fields=['should_change_password'])
        send_email_about_reset_password.s(user, password).apply_async()
        return Response({'status': 'success'})

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsAdminPermissions,),
        serializer_class=ChangeUserActiveSerializer,
    )
    def change_activation(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        detail_serializer = DetailUserSerializer(instance=instance)
        return Response(detail_serializer.data)
