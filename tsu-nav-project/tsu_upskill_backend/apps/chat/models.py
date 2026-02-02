from django.db import models
from django.utils.translation import gettext_lazy as _

class ChatSession(models.Model):
    """Chat session between user and AI"""
    
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='chat_sessions'
    )
    
    title = models.CharField(
        _('Session Title'),
        max_length=255,
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(
        _('Created At'),
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        _('Updated At'),
        auto_now=True
    )
    
    class Meta:
        verbose_name = _('Chat Session')
        verbose_name_plural = _('Chat Sessions')
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.student_id} - {self.title or 'Unnamed'}"
    
    def save(self, *args, **kwargs):
        # Auto-generate title from first message if not provided
        if not self.title:
            first_message = self.messages.first()
            if first_message:
                self.title = first_message.content[:50]
        super().save(*args, **kwargs)


class Message(models.Model):
    """Chat messages"""
    
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
    
    content = models.TextField(
        _('Message Content')
    )
    
    # For AI responses
    is_fallback_to_admin = models.BooleanField(
        _('Fallback to Admin'),
        default=False,
        help_text='AI could not answer, forwarded to admin'
    )
    
    # For admin responses
    admin_user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admin_responses'
    )
    
    created_at = models.DateTimeField(
        _('Created At'),
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.session.user.student_id} - {self.sender}"


class PendingAdminQuestion(models.Model):
    """Questions pending admin response"""
    
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
    
    created_at = models.DateTimeField(
        _('Created At'),
        auto_now_add=True
    )
    
    answered_at = models.DateTimeField(
        _('Answered At'),
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _('Pending Admin Question')
        verbose_name_plural = _('Pending Admin Questions')
        ordering = ['created_at']
    
    def __str__(self):
        return f"Question from {self.message.session.user.student_id}"
