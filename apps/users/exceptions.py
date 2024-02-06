from rest_framework import exceptions


class UserProfileValidatePhotoFieldError(exceptions.ValidationError):
    default_detail = 'Uploaded files exceeded the allowed size'


class MissedLinkUrlAttributeError(ValueError):
    default_detail = 'class attribute `create_new_password_link_url` is not overridden'


class UserValidateEmailFieldError(exceptions.ValidationError):
    default_detail = 'This email is already in use'


class TooSimilarPasswordError(exceptions.ValidationError):
    default_detail = {
        'password': 'The password is too similar to the login',
    }


class CustomerNotFoundError(exceptions.NotFound):
    default_detail = 'Customer does not exists'
