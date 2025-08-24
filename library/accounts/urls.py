from django.urls import path
from .views import CustomLoginAPIView, RegisterAPIView, ProfileAPIView, UserListAPIView, UserUpdateAPIView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('register/', views.register_view, name='register'),
    # path('profile/', views.profile_view, name='profile'),
    # path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', CustomLoginAPIView.as_view(), name='login'),
    path('me/', ProfileAPIView.as_view(), name='profile'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
]