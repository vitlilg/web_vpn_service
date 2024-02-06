from django.conf import settings
from django.utils import timezone
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import BaseAuthentication

from apps.authentications.models.token import Token


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class TokenAuthentication(BaseAuthentication):
    """
    This authentication scheme uses Knox Token for authentication.
    Similar to DRF's TokenAuthentication, it overrides a large amount of that
    authentication scheme to cope with the fact that Tokens are not stored
    in plaintext in the database
    If successful
    - `request.user` will be a django `User` instance
    - `request.auth` will be an `Token` instance
    """
    model = Token
    keyword = 'Token'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        prefix = settings.AUTH_HEADER_PREFIX.encode()

        if not auth:
            return None
        if auth[0].lower() != prefix.lower():
            # Authorization header is possibly for another backend
            return None
        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        user, auth_token = self.authenticate_credentials(auth[1])
        return user, auth_token

    def authenticate_credentials(self, token):
        """
        Due to the random nature of hashing a value, this must inspect
        each auth_token individually to find the correct one.
        Tokens that have expired will be deleted and skipped
        """
        token = token.decode('utf-8')
        try:
            token = Token.objects.select_related('user').get(key=token)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')
        is_expire_token = token.is_expire
        if settings.AUTO_REFRESH and is_expire_token:
            self.renew_token(token)
        elif is_expire_token:
            raise exceptions.AuthenticationFailed('Token was expired.')
        return token.user, token

    def renew_token(self, auth_token):
        current_expiry = auth_token.expiry
        new_expiry = timezone.now() + settings.TOKEN_TTL
        auth_token.expiry = new_expiry
        # Throttle refreshing of token to avoid db writes
        delta = (new_expiry - current_expiry).total_seconds()
        if delta > settings.MIN_REFRESH_INTERVAL:
            auth_token.save(update_fields=('expiry',))

    def authenticate_header(self, request):
        return settings.AUTH_HEADER_PREFIX
