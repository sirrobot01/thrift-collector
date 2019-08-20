from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import login, logout
from rest_framework_jwt.utils import jwt_encode_handler
from django.contrib.auth.models import User
from datetime import datetime
from rest_framework_jwt.settings import api_settings

def jwt_payload_handler(username, password, delta):
    # custom payload handler
    payload = {
        'username': username,
        'password': password,
        'exp': datetime.utcnow() + delta
    }

    return payload

class ObtainJWT(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        # create token
        payload = jwt_payload_handler(username, password, api_settings.JWT_EXPIRATION_DELTA)
        token = jwt_encode_handler(payload)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': "{} is not registered!".format(username)}, status=status.HTTP_404_NOT_FOUND)

        login(request, user)
        return Response({'token': token},
                        status=status.HTTP_200_OK)