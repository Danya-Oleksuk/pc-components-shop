from django.contrib.auth import authenticate, logout
from rest_framework import viewsets, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from .serializers import UserSerializer, UserRegisterSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)