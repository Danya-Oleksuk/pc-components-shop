from rest_framework import serializers
from api.mixins import (
    CreateOnlySerializerMixin,
    ReadOnlySerializerMixin,
    UpdateOnlySerializerMixin,
)
from users.models.users import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

from users.services.crud import (
    user_create,
    user_update,
)


class UserDisplaySerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "created_at",
        )


class TokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password,
        )

        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError({"message": msg}, code="authorization")

        attrs["user"] = user
        return attrs


class UserCreateSerializer(CreateOnlySerializerMixin, serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        style={"input_type": "password"}, required=True, write_only=True
    )
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(_("User with this email already exists"))
        return attrs

    def create(self, validated_data):
        return user_create(**validated_data)


class UserUpdateSerializer(UpdateOnlySerializerMixin, serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        style={"input_type": "password"}, required=True, write_only=True
    )
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        return user_update(user=instance, **validated_data)
