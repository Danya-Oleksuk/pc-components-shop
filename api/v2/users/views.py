from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from api.v2.users.serializers import (
    TokenObtainSerializer,
    UserCreateSerializer,
    UserDisplaySerializer,
    UserUpdateSerializer,
)

from users.models.users import User
from users.services.crud import user_delete


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


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer


class UserUpdateView(GenericAPIView):
    serializer_class = UserUpdateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def path(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDeleteView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk, *args, **kwargs):
        try:
            user = get_object_or_404(User, pk=pk)
            current_user = request.user
            is_admin = current_user.is_staff or current_user.is_superuser

            if not is_admin and user != current_user:
                return Response(
                    {"message": "You do not have permission to delete this user"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            user_delete(user=user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
