"""Views for users' app."""

from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework_jwt.settings import api_settings
import jwt

from .serializers import UserSerializer
from djangular.settings import SECRET_KEY

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class CreateUserView(CreateAPIView):
    """Create user API view."""

    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """Create user and return token."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            print(headers)
            user = self.model.get(username=serializer.data['username'])
            print(user)
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response(
                token,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginUserView(APIView):
    """Log in user API view."""

    def post(self, request, *args, **kwargs):
        """Log in user and return token."""
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            token = {'token': jwt.encode(payload, SECRET_KEY),
                     'status': 'success'
                     }
            return Response(token)
        else:
            token = {'error': 'Invalid credentials',
                     'status': 'failed'
                     }
            return Response(token)
