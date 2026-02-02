from django.db import models
from django.utils.translation import gettext_lazy as _

class LocationCategory(models.Model):
    """Location categories (Building, Classroom, etc.)"""
    name = models.CharField(
        _('Category Name'),
        max_length=100,
        unique=True
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    icon = models.CharField(
        _('Icon'),
        max_length=50,
        blank=True,
        help_text='FontAwesome icon class'
    )
    
    class Meta:
        verbose_name = _('Location Category')
        verbose_name_plural = _('Location Categories')
    
    def __str__(self):
        return self.name


class Location(models.Model):
    """Campus locations with coordinates"""
    
    name = models.CharField(
        _('Location Name'),
        max_length=255
    )
    
    category = models.ForeignKey(
        LocationCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='locations'
    )
    
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )
    
    # GPS Coordinates
    latitude = models.FloatField(
        _('Latitude'),
        help_text='GPS latitude'
    )
    
    longitude = models.FloatField(
        _('Longitude'),
        help_text='GPS longitude'
    )
    
    building_code = models.CharField(
        _('Building Code'),
        max_length=50,
        blank=True,
        null=True
    )
    
    floor = models.IntegerField(
        _('Floor'),
        blank=True,
        null=True
    )
    
    room_number = models.CharField(
        _('Room Number'),
        max_length=50,
        blank=True,
        null=True
    )
    
    image = models.ImageField(
        _('Location Image'),
        upload_to='locations/',
        blank=True,
        null=True
    )
    
    opening_hours = models.CharField(
        _('Opening Hours'),
        max_length=100,
        blank=True,
        null=True
    )
    
    phone_number = models.CharField(
        _('Phone Number'),
        max_length=20,
        blank=True,
        null=True
    )
    
    email = models.EmailField(
        _('Email'),
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField(
        _('Is Active'),
        default=True
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
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.category})" if self.category else self.name


class Bookmark(models.Model):
    """User bookmarked locations"""
    
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='bookmarked_by'
    )
    
    created_at = models.DateTimeField(
        _('Bookmarked At'),
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = _('Bookmark')
        verbose_name_plural = _('Bookmarks')
        unique_together = ('user', 'location')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.student_id} - {self.location.name}"
