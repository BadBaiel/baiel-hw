from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import ConfirmUserCode

class UserLoginValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_password(self, password):
        """custom validation method"""
        return password

class UserCreateValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError("User already exists!")

class ConfirmCodeValidateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    code = serializers.CharField(min_length=6, max_length=6)

    def validate_product_id(self, user_id):
        try:
            ConfirmUserCode.objects.get(id=user_id)
        except ConfirmUserCode.DoesNotExist:
            raise ValidationError(f'Director with id ({user_id}) not found')
        return user_id