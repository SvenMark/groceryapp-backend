from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate

from firebase_admin import auth

# Create your views here.
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from authentication.models import User


class GetLoginToken(APIView):
    """
    View to get a token for a user
    """
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is None:
            response = {
                'status': 'wrong credentials'
            }
            return Response(response, status=HTTP_401_UNAUTHORIZED)

        custom_claims = {
            'is_staff': user.is_staff,
            'avatar_image_url': user.avatar_image_url,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }

        custom_token = auth.create_custom_token(str(user.id), custom_claims)
        response = {"token": custom_token}
        return Response(response)


class CreateUser(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        password_confirm = request.data.get('password_confirm', None)

        if email is None or password is None or password_confirm is None:
            response = {
                'status': 'Please set all fields'
            }
            return Response(response, status=HTTP_400_BAD_REQUEST)

        if not password == password_confirm:
            response = {
                'status': 'Please make sure both passwords match'
            }
            return Response(response, status=HTTP_400_BAD_REQUEST)

        try:
            User.objects.get(email=email)
            response = {
                'status': 'This email already has an account'
            }
            return Response(response, status=HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            pass
        user = User.objects.create_user(email, password)

        custom_claims = {
            'is_staff': user.is_staff,
            'avatar_image_url': user.avatar_image_url,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }

        custom_token = auth.create_custom_token(str(user.id), custom_claims)
        response = {"token": custom_token}
        return Response(response)
