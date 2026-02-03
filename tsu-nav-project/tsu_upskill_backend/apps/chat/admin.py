from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import ChatSession, Message, PendingAdminQuestion

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'title', 'message_count_badge', 'last_active', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__student_id', 'user__email', 'title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',) # เรียงตามการเคลื่อนไหวล่าสุด

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

    def content_preview(self, obj):
        # แสดงข้อความแบบเต็มเมื่อเอาเมาส์ไปชี้ (Tooltip)
        return format_html('<span title="{}">{}</span>', obj.content, (obj.content[:40] + '...') if len(obj.content) > 40 else obj.content)
    content_preview.short_description = 'เนื้อหาข้อความ'

    def sender_style(self, obj):
        styles = {
            'user': ('#ff8c00', 'USER'),
            'ai': ('#0056b3', 'GEMINI AI'),
            'admin': ('#722ed1', 'ADMIN JAMES'),
        }
        color, label = styles.get(obj.sender, ('#000', obj.sender))
        return format_html('<span style="color: {}; font-weight: bold;">● {}</span>', color, label)
    sender_style.short_description = 'ผู้ส่ง'

    def is_fallback_badge(self, obj):
        if obj.is_fallback_to_admin:
            return format_html('<span style="color: #f5222d; animation: pulse 2s infinite;">⚠️ รอแอดมิน</span>')
        return format_html('<span style="color: #52c41a;">✓ เรียบร้อย</span>')
    is_fallback_badge.short_description = 'สถานะ'

@admin.register(PendingAdminQuestion)
class PendingAdminQuestionAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'question_text', 'status_badge', 'view_chat_link', 'created_at')
    list_filter = ('status', 'created_at')
    list_editable = ('status',) # พี่สามารถเปลี่ยนสถานะได้จากหน้าลิสต์เลย!
    search_fields = ('message__session__user__student_id', 'message__content')
    
    def question_text(self, obj):
        # ดึงข้อความที่เด็กถามมาโชว์เลย ไม่ต้องกดเข้าไปดู
        return obj.message.content
    question_text.short_description = 'คำถามที่ AI ตอบไม่ได้'

    def status_badge(self, obj):
        if obj.status == 'pending':
            return format_html('<b style="color: #faad14;">⏳ กำลังรอ</b>')
        return format_html('<b style="color: #52c41a;">✅ ตอบแล้ว</b>')
    status_badge.short_description = 'สถานะ'

    def view_chat_link(self, obj):
        url = reverse('admin:chat_chatsession_change', args=[obj.message.session.id])
        return format_html('<a class="button" href="{}" style="background: linear-gradient(45deg, #0056b3, #00a1ff); color: white; padding: 4px 12px; border-radius: 6px; border: none; font-weight: bold; text-decoration: none;">เข้าสู่แชท</a>', url)
    view_chat_link.short_description = 'จัดการ'
