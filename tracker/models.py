from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MaxValueValidator
from custom_translate.templatetags.persian_calendar_convertor import convert_to_persian_calendar, format_persian_datetime

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

class Category(models.Model):
    name = models.CharField(max_length=15, unique=True)
    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('income', 'درآمد'),
        ('expense', 'خرج'),
    )
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=8, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.IntegerField( validators=[MaxValueValidator(999999999999)])
    date = models.DateTimeField()
    def __str__(self):
        return f"user: {self.user} - on: {self.date}"
    @property
    def persian_date(self):
        return format_persian_datetime(convert_to_persian_calendar(self.date))