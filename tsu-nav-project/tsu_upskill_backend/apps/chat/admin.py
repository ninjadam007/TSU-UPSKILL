from django.contrib import admin
from django.utils.html import format_html
from .models import ChatSession, Message, PendingAdminQuestion

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'message_count_badge', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__student_id', 'user__email', 'title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',) # ให้แชทล่าสุดอยู่บนสุด

    def message_count_badge(self, obj):
        count = obj.messages.count()
        return format_html('<span style="font-weight: bold; color: #0056b3;">{} ข้อความ</span>', count)
    message_count_badge.short_description = 'จำนวนข้อความ'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'sender_style', 'is_fallback_badge', 'content_snippet', 'created_at')
    list_filter = ('sender', 'is_fallback_to_admin', 'created_at')
    search_fields = ('session__user__student_id', 'content')
    readonly_fields = ('created_at',)

    def sender_style(self, obj):
        color = "#ff8c00" if obj.sender == 'user' else "#0056b3"
        return format_html('<b style="color: {};">{}</b>', color, obj.get_sender_display())
    sender_style.short_description = 'ผู้ส่ง'

    def is_fallback_badge(self, obj):
        if obj.is_fallback_to_admin:
            return format_html('<span style="background: #ff4d4f; color: white; padding: 2px 8px; border-radius: 10px;">ต้องดูแล</span>')
        return "AI ตอบแล้ว"
    is_fallback_badge.short_description = 'สถานะ AI'

    def content_snippet(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_snippet.short_description = 'ข้อความ'

    def get_user(self, obj):
        return obj.session.user.student_id
    get_user.short_description = 'รหัสนิสิต'

@admin.register(PendingAdminQuestion)
class PendingAdminQuestionAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'status_badge', 'created_at', 'answered_at')
    list_filter = ('status', 'created_at')
    search_fields = ('message__session__user__student_id',)
    readonly_fields = ('created_at',)
    actions = ['mark_as_answered'] # เพิ่มคำสั่งลัดสำหรับแอดมิน

    def status_badge(self, obj):
        colors = {'pending': '#faad14', 'answered': '#52c41a'}
        return format_html('<b style="color: {}; text-transform: uppercase;">{}</b>', 
                           colors.get(obj.status, 'black'), obj.status)
    status_badge.short_description = 'สถานะ'

    def get_user(self, obj):
        return obj.message.session.user.student_id
    get_user.short_description = 'รหัสนิสิต'

    @admin.action(description='ทำเครื่องหมายว่าตอบแล้ว')
    def mark_as_answered(self, request, queryset):
        queryset.update(status='answered')
