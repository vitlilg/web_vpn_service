from rest_framework import generics, parsers, permissions
from rest_framework.response import Response

from apps.users.api.v1.serializers.user_profile import UserProfileUploadPhotoSerializer
from apps.users.services.user_profile import UserProfileService
from apps.web_cabinet.api.v1.serializers.web_user_profile import UserInfoSerializer


class GetUserInfoView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user


class UploadUserPhotoView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)
    serializer_class = UserProfileUploadPhotoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = request.user
        UserProfileService.upload_user_photo(request, user_obj.userprofile)
        return Response({'status': 'success'})
