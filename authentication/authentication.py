from authentication.models import User
from firebase_admin.auth import AuthError
from rest_framework import authentication, HTTP_HEADER_ENCODING
from rest_framework import exceptions

from firebase_admin import auth


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        header = get_header(request)

        if header is None:
            return None

        token = get_raw_token(header)

        if not token:
            return None

        try:
            custom_token = auth.verify_id_token(token.decode(), check_revoked=True)
            user = User.objects.get(pk=custom_token.get('uid'))
            return user, None
        except ValueError:
            raise exceptions.AuthenticationFailed('Token is invalid')
        except AuthError:
            raise exceptions.AuthenticationFailed('Token is revoked')


def get_header(request):
    """
    Extracts the header containing the JSON web token from the given
    request.
    """
    header = request.META.get('HTTP_AUTHORIZATION')

    if isinstance(header, str):
        # Work around django test client oddness
        header = header.encode(HTTP_HEADER_ENCODING)

    return header


def get_raw_token(header):
    """
    Extracts an unvalidated JSON web token from the given "Authorization"
    header value.
    """
    parts = header.split()

    if len(parts) == 0:
        # Empty AUTHORIZATION header sent
        return None

    if str(parts[0]) != "b'Bearer'":
        # Assume the header does not contain a JSON web token
        return None

    if len(parts) != 2:
        raise exceptions.AuthenticationFailed(
            _('Authorization header must contain two space-delimited values'),
            code='bad_authorization_header',
        )

    return parts[1]
