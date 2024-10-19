from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, contact_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        if not contact_number:
            raise ValueError('The Contact Number field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, contact_number=contact_number, **extra_fields)
        user.set_password(password)
        user.is_active = False  # Users are inactive until approved by admin
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, contact_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, contact_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    contact_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=False)  # Active status to be set by admin
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'contact_number']

    def __str__(self):
        return self.email

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  # Allow null for anonymous posts
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username if self.user else 'Anonymous'}"

class Report(models.Model):
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports')
    reported_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    reported_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reported_by.username}"

class UserPreference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Dark Mode' if self.dark_mode else 'Light Mode'}"
