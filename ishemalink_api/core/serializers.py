from django.contrib.auth import get_user_model
from rest_framework import serializers

from .validators import validate_nid

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "phone", "password", "user_type", "assigned_sector", "nid_number"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.full_clean()
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "user_type", "assigned_sector", "is_verified"]


class NIDVerifySerializer(serializers.Serializer):
    nid = serializers.CharField()

    def validate_nid(self, value):
        if not validate_nid(value):
            raise serializers.ValidationError("Invalid NID format. Must be 16 numeric digits starting with 1.")
        return value
