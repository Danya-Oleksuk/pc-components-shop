from rest_framework import serializers
from api.mixins import (
    ReadOnlySerializerMixin,
)
from users.models.users import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate


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
