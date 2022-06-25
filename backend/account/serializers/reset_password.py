import re
import base64
import jwt

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from account.models.reset_password import ResetPasswordRequest

from account.models.user import CustomUser


valid_password_pattern = re.compile(
    "^(?=.*\d)(?=.*[!@#$%^&*~])(?=.*[a-z])(?=.*[A-Z]).{8,}$")


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def save(self):
        """
        We do not want to give out detailed information to not aid
        hackers
        """
        email = self.validated_data.get("email", None)
        if email and not CustomUser.objects.filter(email=email.lower()).exists():
            return
        user = CustomUser.objects.get(email=email.lower())
        instance = ResetPasswordRequest.objects.create(user=user)
        # send email to user
        user.send_email()
        return


class ValidateResetRequest(serializers.Serializer):
    secret = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(max_length=64, required=True)

    def validate_password(self, value):
        if valid_password_pattern.match(value) is None:
            raise serializers.ValidationError(
                "Password must contain numbers, symbols, \
                    upper and lower case letters and should \
                        at least be of 8 characters")
        return value

    def verify(self, validated_data):
        response = {"successful": True, }

        secret = settings.SECRET_KEY
        secret_bytes = secret.encode('ascii')
        encryption_secret = base64.b64encode(secret_bytes)

        decoded_request = None

        try:
            decoded_request = jwt.decode(
                validated_data.get("secret"),
                encryption_secret,
                algorithms=["HS256"]
            )
        except Exception as e:
            # logger.error(e)
            raise serializers.ValidationError("Kindly check, the secret key is not valid!")

        if decoded_request is not None:
            reset_object = ResetPasswordRequest.objects.filter(
                pk=decoded_request["request_id"],
                expired=False,
                used=False
            ).first()
            if reset_object:

                reset_object.user.set_password(validated_data.get("password"))
                reset_object.user.save()
                reset_object.used = True
                reset_object.save()
            else:
                raise serializers.ValidationError("Your request to change password has " \
                    "expired. Kindly generate a new password reset request.")

        return response
