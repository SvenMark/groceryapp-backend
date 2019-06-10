from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate

from firebase_admin import auth

# Create your views here.
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
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
            return Response('wrong credentials')

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
    def post(self, request, format=None):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        password_confirm = request.data.get('password_confirm', None)

        if email is None or password is None or password_confirm is None:
            return Response('Please set all fields')

        if not password == password_confirm:
            return Response('Please make sure both passwords match')

        try:
            User.objects.get(email=email)
            return Response('This email already has an account')
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
