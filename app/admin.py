from django.contrib import admin
from .models import CustomUser, Post, Report, UserPreference

admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Report)
admin.site.register(UserPreference)