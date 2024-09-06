from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MaxValueValidator
from custom_translate.templatetags.persian_calendar_convertor import convert_to_persian_calendar, format_persian_date, format_persian_datetime, convert_to_persian_calendar_date
from .managers import TransactionQuerySet

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
    username = None 
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()  
    def __str__(self):  
        return self.email
    
    @property
    def persian_date_joined(self):
        return format_persian_date(convert_to_persian_calendar_date(self.date_joined))

class Category(models.Model):
    name = models.CharField(max_length=15, unique=True)
    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('income', 'درآمد'),
        ('expense', 'هزینه'),
    )
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='دسته بندی')
    type = models.CharField(max_length=8, choices=TRANSACTION_TYPE_CHOICES,verbose_name='نوع')
    amount = models.IntegerField( validators=[MaxValueValidator(999999999999)],verbose_name='مقدار')
    date = models.DateField(verbose_name='تاریخ')
    objects = TransactionQuerySet.as_manager()

    def __str__(self):
        return f"user: {self.user} - on: {self.date}"
    
    @property
    def persian_date(self):
        return format_persian_date(convert_to_persian_calendar_date(self.date))
    
    @property
    def formated_amount(self):
        return f'تومان {self.amount:,}'
    
    class Meta:
        ordering = ['-date']