from rest_framework import serializers 
from .models import CustomUser, UserProfile
from django.contrib.auth import authenticate 

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role', 'date_of_membership']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'], 
            role=validated_data.get('role', 'member')
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile 
        fields = ['bio', 'profile_picture']

#so here we could have used obtain_auth_token but we created our cutom login serializer 

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField() 
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return {"user": user} 
        
        raise serializers.ValidationError("Incorrect credentials")