from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username , email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email is required")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True) 
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  ##here you arre calling , saving and hashing your password atthe same time
        user.save(using=self._db) 
        return user 
    
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True) 

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_users(username, email, password, **extra_fields)

class CustomUser(AbstractUser):  
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True
    )
    ROLECHOICES = [
        ("ADMIN", "Admin"), 
        ("LIBRARIAN", "Librarian"),
        ("MEMBER", "Member")
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True) 
    date_of_membership = models.DateField(auto_now_add=True)
    active_status = models.BooleanField(default=True)
    role = models.CharField(max_length=100, choices=ROLECHOICES, default="MEMBER") 

    objects = CustomUserManager()
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username' 

    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="userprofile")
    bio = models.TextField(blank=True, null=True) 
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return self.user.username