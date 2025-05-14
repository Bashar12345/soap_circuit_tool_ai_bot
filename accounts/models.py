import enum 

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.conf import settings


class CustomUserManager(UserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=True, is_superuser=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):

    # ROLE = [
    #     ('student', 'Student'),
    #     ('hostler', 'Hostler'),
    #     ('entrepreneur', 'Entrepreneur'),
    #     ('educator', 'Educator'),
    #     ('strategist', 'Strategist'),
    # ]

    username = models.CharField(max_length=150, unique=True) 
    email = models.EmailField(blank=True, null=True)
    
    image = models.ImageField(upload_to='users_images/', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    # role = models.CharField(max_length=50, choices=ROLE)

    otp = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)
    
    # is_subscribed = models.BooleanField(default=False)
    
    # stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)

    # USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()






