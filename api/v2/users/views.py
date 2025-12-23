from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.v2.users.serializers import (
    UserDisplaySerializer,
)

from users.models.users import User


class UserListApi(ListAPIView):
    serializer_class = UserDisplaySerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    search_fields = (
        "id",
        "email",
        "first_name",
        "last_name",
    )
