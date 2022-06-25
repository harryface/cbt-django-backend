from drf_spectacular.utils import extend_schema
from rest_framework import (
    viewsets, permissions, decorators, response)

from account.serializers.reset_password import (
    ResetPasswordSerializer, ValidateResetRequest)


class PasswordResetViewSet(viewsets.ViewSet):
    '''
    For password reset request, basically takes an email
    and if exists send the appropriate mail.
    '''
    
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            {"message": "if your account exists, we have sent you a mail"})

    @extend_schema(request=ValidateResetRequest)
    @decorators.action(detail=False, methods=["POST"])
    def change_password(self, request):
        """
        Receive the secret key from the query param and post it
        alongside the new password to the backend
        """
        serializer = ValidateResetRequest(data=request.data)
        
        if serializer.is_valid():
            serializer.verify()
            return response.Response(
                {"success": "Passwod changed successfully."})
        else:
            return response.Response(serializer.errors)
