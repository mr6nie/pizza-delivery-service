from click import password_option

from pizza.settings import DJOSER
from django.db import IntegrityError
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from phonenumber_field.serializerfields import PhoneNumberField

from .models import User


class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=80)
    phone_number = PhoneNumberField(allow_null=False, allow_blank=False)
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "password"]

    def validate(self, attrs):
        username_exists = User.objects.filter(username=attrs["username"]).exists()

        if username_exists:
            raise serializers.ValidationError(detail="User with username exists")

        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise serializers.ValidationError(detail="User with email exists")

        phonenumber_exists = User.objects.filter(
            phone_number=attrs["phone_number"]
        ).exists()

        if phonenumber_exists:
            raise serializers.ValidationError(detail="User with phone number exists")

        return super().validate(attrs)

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        if DJOSER.SEND_ACTIVATION_EMAIL:
            user.is_active = False
            user.save(update_fields=["is_active"])
        return user


# class UserCreationSerializer(UserCreateSerializer):
#     phone_number = PhoneNumberField(allow_null=False, allow_blank=False)

#     class Meta(UserCreateSerializer.Meta):
#         model = User
#         fields = ["id", "username", "email", "phone_number", "password"]
