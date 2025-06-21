from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)  # changed from confirm_password

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role', 'mobile_no',
            'password', 'password2', 'first_name', 'last_name'  # changed confirm_password to password2
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data.pop('password2', None)  # changed confirm_password to password2
        return super().create(validated_data)

class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid credentials")


