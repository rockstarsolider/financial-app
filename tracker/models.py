from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission  
from django.db import models
from django_jalali.db import models as jmodels

class CustomUserManager(BaseUserManager):  
    def create_user(self, email, password=None, **extra_fields):  
        if not email:  
            raise ValueError('The Email field must be set')  
        email = self.normalize_email(email)  
        user = self.model(email=email, **extra_fields)  
        user.set_password(password)  
        user.save(using=self._db)  
        return user
    def create_superuser(self, email, password=None, **extra_fields):  
        """Create and return a superuser with the given email and password."""  
        extra_fields.setdefault('is_staff', True)  
        extra_fields.setdefault('is_superuser', True)  

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):  
    username = None  # Remove the username field  
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # Use email as the unique identifier  
    REQUIRED_FIELDS = []  # No additional fields are required during user creation  

    objects = CustomUserManager()  
    def __str__(self):  
        return self.email