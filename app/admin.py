from django.contrib import admin
from .models import Tweet, CustomUser, Comment, Notification

# Register your models here.
admin.site.register(Tweet)


@admin.register(CustomUser)  # Register CustomUser instead of User
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser  # Use the custom user model here
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    ordering = ('username',)


admin.site.register(Comment)

admin.site.register(Notification)