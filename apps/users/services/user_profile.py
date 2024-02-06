from rest_framework.request import Request

from apps.users.models import UserProfile
from generic.tasks import convert_model_image_to_webp_format


class UserProfileService:

    @staticmethod
    def upload_user_photo(request: Request, user_profile: UserProfile) -> None:
        request_files = request.FILES.getlist('photo')
        user_profile.photo = request_files[0]
        user_profile.save(update_fields=['photo'])
        convert_model_image_to_webp_format.delay(user_profile, 'photo')
