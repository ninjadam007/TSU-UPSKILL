from django.db import models
from django.utils.translation import gettext_lazy as _

class ChatSession(models.Model):
    """บทสนทนาระหว่างนิสิตและ AI"""
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='chat_sessions'
    )
    title = models.CharField(
        _('Session Title'),
        max_length=255,
        blank=True,
        null=True,
        help_text="หัวข้อการสนทนา (จะถูกสร้างอัตโนมัติจากข้อความแรก)"
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Chat Session')
        verbose_name_plural = _('Chat Sessions')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.student_id} - {self.title or 'ไม่มีชื่อ'}"

    def update_title_from_first_message(self):
        """ฟังก์ชันช่วยสำหรับอัปเดตหัวข้อจากข้อความแรก"""
        if not self.title:
            first_msg = self.messages.all().order_by('created_at').first()
            if first_msg:
                self.title = (first_msg.content[:47] + '...') if len(first_msg.content) > 50 else first_msg.content
                self.save(update_fields=['title'])


class Message(models.Model):
    """ข้อความในแต่ละแชท"""
    SENDER_USER = 'user'
    SENDER_AI = 'ai'
    SENDER_ADMIN = 'admin'
    
    SENDER_CHOICES = [
        (SENDER_USER, _('User')),
        (SENDER_AI, _('AI Bot')),
        (SENDER_ADMIN, _('Admin')),
    ]
    
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.CharField(
        _('Sender'),
        max_length=10,
        choices=SENDER_CHOICES
    )
    content = models.TextField(_('Message Content'))
    
    # กรณี AI ตอบไม่ได้
    is_fallback_to_admin = models.BooleanField(
        _('Fallback to Admin'),
        default=False,
        help_text='AI ตอบไม่ได้ และส่งต่อให้แอดมินแล้ว'
    )
    
    # ถ้าแอดมินเป็นคนตอบ ให้เก็บชื่อแอดมินไว้ด้วย
    admin_user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admin_responses'
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['created_at'] # เรียงจากเก่าไปใหม่ตามลำดับการแชท

    def __str__(self):
        return f"{self.session.user.student_id} - {self.sender}"


class PendingAdminQuestion(models.Model):
    """คำถามที่รอให้แอดมิน James มาตอบ"""
    STATUS_PENDING = 'pending'
    STATUS_ANSWERED = 'answered'
    STATUS_CLOSED = 'closed'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_ANSWERED, _('Answered')),
        (STATUS_CLOSED, _('Closed')),
    ]
    
    message = models.OneToOneField(
        Message,
        on_delete=models.CASCADE,
        related_name='pending_question'
    )
    status = models.CharField(
        _('Status'),
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    answered_at = models.DateTimeField(_('Answered At'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('Pending Admin Question')
        verbose_name_plural = _('Pending Admin Questions')
        ordering = ['created_at']

    def __str__(self):
        return f"Q: {self.message.session.user.student_id} ({self.status})"
