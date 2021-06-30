import jwt, datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from cbt import settings
from account.models import CustomUser


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        is_examiner = 'api/examiner' in request.path

        token = request.COOKIES.get('jwt')

        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('unauthenticated')

        if (is_examiner and payload['scope'] != 'examiner') or (not is_examiner and payload['scope'] != 'taker'):
            raise exceptions.AuthenticationFailed('Invalid Scope!')

        user = CustomUser.objects.get(pk=payload['user_id'])

        if user is None:
            raise exceptions.AuthenticationFailed('CustomUser not found!')

        return (user, None)

    @staticmethod
    def generate_jwt(id, scope):
        payload = {
            'user_id': id,
            'scope': scope,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')