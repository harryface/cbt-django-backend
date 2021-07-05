from rest_framework import exceptions, permissions, response, status
from rest_framework.views import APIView

from .models import CustomUser
from cbt.authentication import JWTAuthentication
from .serializers import UserSerializer


class RegisterAPIView(APIView):
    '''View for registration for both examiner and exam taker'''

    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')

        data['is_examiner'] = 'examiner' in request.path

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)


class LoginAPIView(APIView):
    '''View for logging the examiner or the exam taker in'''

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect Password!')

        scope = 'examiner' if 'examiner' in request.path else 'taker'

        if user.is_examiner and scope == 'taker':
            raise exceptions.AuthenticationFailed('Unauthorized')

        token = JWTAuthentication.generate_jwt(user.id, scope)

        response_ = response.Response()
        response_.set_cookie(key='jwt', value=token, httponly=True)
        response_.data = {
            'message': 'success'
        }

        return response_


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, _):
        response_ = response.Response()
        response_.delete_cookie(key='jwt')
        response_.data = {
            'message': 'success'
        }
        return response_


class UserDetailAPIView(APIView):
    '''A view for getting the user data'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = UserSerializer(user).data

        return response.Response(data)


class UserInfoUpdateAPIView(APIView):
    '''A view for getting the user data'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)


class UserPasswordUpdateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')

        user.set_password(data['password'])
        user.save()
        return response.Response(UserSerializer(user).data)


class UsersDetailAPIView(APIView):
    '''A view for getting all user data'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, _):
        user = CustomUser.objects.all()
        if user:
            serializer = UserSerializer(user, many=True)
            return response.Response(serializer.data)
        return response.Response(
            {"error": "No user exists"}, status=status.HTTP_404_NOT_FOUND)