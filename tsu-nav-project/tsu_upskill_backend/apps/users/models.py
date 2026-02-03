import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    """โมเดลผู้ใช้งานหลัก (เน้นนิสิต TSU)"""
    
    STUDENT = 'student'
    ADMIN = 'admin'
    STAFF = 'staff' # เพิ่มเผื่อไว้สำหรับเจ้าหน้าที่คณะ
    
    ROLE_CHOICES = [
        (STUDENT, _('Student')),
        (STAFF, _('Staff')),
        (ADMIN, _('Admin')),
    ]
    
    # บังคับรหัสนิสิต 10 หลัก (เช่น 6410xxxxxx)
    student_id = models.CharField(
        _('Student ID'),
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message=_('รหัสนิสิตต้องเป็นตัวเลข 10 หลักเท่านั้น'),
                code='invalid_student_id'
            )
        ]
    )
    
    # บังคับใช้อีเมลมหาวิทยาลัยเท่านั้น
    email = models.EmailField(
        _('Email Address'),
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w\.-]+@tsu\.ac\.th$',
                message=_('กรุณาใช้อีเมล @tsu.ac.th เท่านั้น'),
                code='invalid_email_domain'
            )
        ]
    )
    
    role = models.CharField(_('Role'), max_length=10, choices=ROLE_CHOICES, default=STUDENT)
    is_email_verified = models.BooleanField(_('Email Verified'), default=False)
    phone_number = models.CharField(_('Phone Number'), max_length=20, blank=True, null=True)
    department = models.CharField(_('Department'), max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(_('Profile Picture'), upload_to='profile_pictures/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student_id} - {self.get_full_name() or self.username}"
    
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser


class EmailVerificationToken(models.Model):
    """โมเดลเก็บ Token สำหรับยืนยันตัวตนผ่านอีเมล"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='verification_token'
    )
    token = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        # ถ้ายังไม่มีเวลาหมดอายุ ให้ตั้งไว้ที่ 24 ชั่วโมงหลังจากสร้าง
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Token for {self.user.email} (Expired: {self.is_expired})"
