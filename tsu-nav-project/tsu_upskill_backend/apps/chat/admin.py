from django.contrib import admin
from django.utils.html import format_html
from .models import ChatSession, Message, PendingAdminQuestion

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'title', 'message_count_badge', 'last_active', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__student_id', 'user__email', 'title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)

    def user_link(self, obj):
        return format_html('<b style="color: #0056b3;">{}</b>', obj.user.student_id)
    user_link.short_description = 'รหัสนิสิต'

    def message_count_badge(self, obj):
        count = obj.messages.count()
        color = "#52c41a" if count > 5 else "#1890ff"
        return format_html('<span style="background: {}; color: white; padding: 2px 10px; border-radius: 12px; font-size: 11px;">{} msg</span>', color, count)
    message_count_badge.short_description = 'จำนวนข้อความ'

    def last_active(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        return last_msg.created_at if last_msg else obj.updated_at
    last_active.short_description = 'เคลื่อนไหวล่าสุด'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'sender_style', 'content_preview', 'is_fallback_badge', 'created_at')
    list_filter = ('sender', 'is_fallback_to_admin', 'created_at')
    search_fields = ('session__user__student_id', 'content')
    readonly_fields = ('created_at',)

    def get_user(self, obj):
        return obj.session.user.student_id
    get_user.short_description = 'นิสิต'

    def content_preview(self, obj):
        content = obj.content[:40] + '...' if len(obj.content) > 40 else obj.content
        return format_html('<span title="{}">{}</span>', obj.content, content)
    content_preview.short_description = 'เนื้อหา'

    def sender_style(self, obj):
        styles = {'user': '#ff8c00', 'ai': '#0056b3', 'admin': '#722ed1'}
        color = styles.get(obj.sender, '#000')
        return format_html('<span style="color: {}; font-weight: bold;">● {}</span>', color, obj.sender.upper())
    sender_style.short_description = 'ผู้ส่ง'

    def is_fallback_badge(self, obj):
        if obj.is_fallback_to_admin:
            return format_html('<span style="color: #f5222d;">⚠️ รอแอดมิน</span>')
        return format_html('<span style="color: #52c41a;">✓ เรียบร้อย</span>')
    is_fallback_badge.short_description = 'สถานะ'

@admin.register(PendingAdminQuestion)
class PendingAdminQuestionAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'question_text', 'status', 'status_badge', 'created_at')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = ('message__session__user__student_id',)

    def get_user(self, obj):
        return obj.message.session.user.student_id
    get_user.short_description = 'นิสิต'

    def question_text(self, obj):
        return obj.message.content
    question_text.short_description = 'คำถาม'

    def status_badge(self, obj):
        color = "#faad14" if obj.status == 'pending' else "#52c41a"
        label = "⏳ รอตอบ" if obj.status == 'pending' else "✅ ตอบแล้ว"
        return format_html('<b style="color: {};">{}</b>', color, label)
    status_badge.short_description = 'Badge'
