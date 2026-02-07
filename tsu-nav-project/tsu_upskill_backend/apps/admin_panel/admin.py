from django.contrib import admin
from apps.chat.models import Message, PendingAdminQuestion 
from .models import SystemAnnouncement 

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'content', 'created_at')
    list_filter = ('sender', 'created_at')

@admin.register(PendingAdminQuestion)
class PendingAdminQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'answered_at')
    list_editable = ('status',) 
    list_filter = ('status', 'created_at')

@admin.register(SystemAnnouncement)
class SystemAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
