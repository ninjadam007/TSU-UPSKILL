from django.contrib import admin
from .models import CustomUser, EmailVerificationToken

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'email', 'get_full_name', 'role', 'is_email_verified', 'created_at')
    list_filter = ('role', 'is_email_verified', 'created_at')
    search_fields = ('student_id', 'email', 'first_name', 'last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture')
        }),
        ('TSU Info', {
            'fields': ('student_id', 'department')
        }),
        ('Account Status', {
            'fields': ('role', 'is_email_verified', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_login'),
            'classes': ('collapse',)
        }),
    )

@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'expires_at')
    list_filter = ('created_at',)
    search_fields = ('user__email',)
    readonly_fields = ('created_at',)
