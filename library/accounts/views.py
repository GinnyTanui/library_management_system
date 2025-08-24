from django.shortcuts import render
from .forms import CustomUserCreationForm, UserProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, UserSerializer, UserProfileSerializer
from rest_framework import generics 
from .permissions import isAdmin 
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, UserProfile
from rest_framework.authtoken.views import ObtainAuthToken


class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can register

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Registration successful.',
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


class CustomLoginAPIView(ObtainAuthToken):
    serializer_class = LoginSerializer   

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "role": user.role
        })


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile


class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all() 
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, isAdmin] 

class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, isAdmin] 

