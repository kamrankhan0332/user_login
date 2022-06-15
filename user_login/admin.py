from django.contrib import admin
from .models import User, UserSession, UserProfile

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(UserSession)
