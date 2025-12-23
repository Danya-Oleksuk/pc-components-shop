from rest_framework import serializers
from api.mixins import (
    ReadOnlySerializerMixin,
)
from users.models.users import User


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
