from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken

from api.v2.users.serializers import (
    TokenObtainSerializer,
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


class UserApiView(RetrieveAPIView):
    serializer_class = UserDisplaySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class AuthTokenObtainView(ObtainAuthToken):
    serializer_class = TokenObtainSerializer
