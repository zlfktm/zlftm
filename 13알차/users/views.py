from django.contrib.auth import get_user_model, login
from django.shortcuts import render, get_object_or_404

from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from users.serializers import UserSerializer, UserDetailSerializer, UserLoginSerializer

User = get_user_model()

class UserSignupView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request) :
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid() :
            login(request, serializer.validated_data['user'])
            return Response({'message' : 'User logged in'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)