import re
from rest_framework import serializers
from django.db import transaction

from account.models.user import CustomUser


valid_contact_no_pattern = re.compile(
    "^\+?\d?(?:(?:[\+]?(?:[\d]{1,3}(?:[ ]+|[\-.])))?[(]?(?:[\d]{3})[\-/)]?(?:[ ]+)?)?(?:[a-zA-Z2-9][a-zA-Z0-9 \-.]{6,})(?:(?:[ ]+|[xX]|(i:ext[\.]?)){1,2}(?:[\d]{1,5}))?$")
valid_password_pattern = re.compile(
    "^(?=.*\d)(?=.*[!@#$%^&*~])(?=.*[a-z]).{8,}$")


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name',
                  'email', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True}}

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError(
                "An account with the same email already exists")
        return value

    def validate_password(self, value):
        if valid_password_pattern.match(value) is None:
            raise serializers.ValidationError(
                "Password must contain numbers, symbols, letters"
                " and should at least be of 8 characters")
        return value

    def validate(self, attrs):
        password2 = attrs.pop('password_confirm', None)
        if attrs['password'] != password2:
            raise serializers.ValidationError("Passwords do not match!")
        return attrs

    def create(self, validated_data):
        """
        create a cart and profile object alongside
        """
        password = validated_data.pop('password', None)

        with transaction.atomic():
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            instance.save()

        return instance
