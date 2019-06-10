from django.shortcuts import render
from django.contrib.auth import authenticate

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

# Create your views here.
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework.views import APIView

from authentication.models import User

cred = credentials.Certificate("secrets/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


class GetLoginToken(APIView):
    """
    View to get a token for a user
    """

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
