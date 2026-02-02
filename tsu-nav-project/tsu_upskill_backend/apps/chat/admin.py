from django.contrib import admin
from .models import ChatSession, Message, PendingAdminQuestion

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'message_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__student_id', 'title')
    readonly_fields = ('created_at', 'updated_at')
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'sender', 'is_fallback_to_admin', 'created_at')
    list_filter = ('sender', 'is_fallback_to_admin', 'created_at')
    search_fields = ('session__user__student_id', 'content')
    readonly_fields = ('created_at',)
    
    def get_user(self, obj):
        return obj.session.user.student_id
    get_user.short_description = 'User'

@admin.register(PendingAdminQuestion)
class PendingAdminQuestionAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'status', 'created_at', 'answered_at')
    list_filter = ('status', 'created_at')
    search_fields = ('message__session__user__student_id',)
    readonly_fields = ('created_at',)
    
    def get_user(self, obj):
        return obj.message.session.user.student_id
    get_user.short_description = 'User'
