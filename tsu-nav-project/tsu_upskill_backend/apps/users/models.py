from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """Custom User model with student ID"""
    
    STUDENT = 'student'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (STUDENT, _('Student')),
        (ADMIN, _('Admin')),
    ]
    
    student_id = models.CharField(
        _('Student ID'),
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Student ID must be 10 digits',
                code='invalid_student_id'
            )
        ]
    )
    
    email = models.EmailField(
        _('Email Address'),
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w\.-]+@tsu\.ac\.th$',
                message='Email must be @tsu.ac.th domain',
                code='invalid_email_domain'
            )
        ]
    )
    
    role = models.CharField(
        _('Role'),
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT
    )
    
    is_email_verified = models.BooleanField(
        _('Email Verified'),
        default=False
    )
    
    phone_number = models.CharField(
        _('Phone Number'),
        max_length=20,
        blank=True,
        null=True
    )
    
    department = models.CharField(
        _('Department'),
        max_length=100,
        blank=True,
        null=True
    )
    
    profile_picture = models.ImageField(
        _('Profile Picture'),
        upload_to='profile_pictures/',
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
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student_id} - {self.get_full_name()}"
    
    def is_admin(self):
        return self.role == self.ADMIN


class EmailVerificationToken(models.Model):
    """Email verification token"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='verification_token'
    )
    token = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"Verification token for {self.user.email}"
