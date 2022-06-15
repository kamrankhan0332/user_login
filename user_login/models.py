from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import UserManager


class User(AbstractBaseUser, UserManager):
    username = models.CharField(max_length=1024, unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=1024, null=True, blank=True)
    email = models.CharField(max_length=1024, null=True, blank=True)
    # admin = 1
    # celebrity = 2
    # end_user = 3
    user_type = models.IntegerField(default=3)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # objects = models.Manager()
    objects = UserManager()
    USERNAME_FIELD = 'username'
    to_create = UserManager()

    def has_module_perms(self, app_label):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return self.is_superuser


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=1024, null=True, blank=True)


class UserSession(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)