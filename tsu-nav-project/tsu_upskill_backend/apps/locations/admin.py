from django.contrib import admin
from .models import Location, LocationCategory, Bookmark

@admin.register(LocationCategory)
class LocationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'building_code', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'building_code', 'room_number', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'category', 'description', 'image')
        }),
        ('Location Details', {
            'fields': ('building_code', 'floor', 'room_number', 'latitude', 'longitude')
        }),
        ('Contact', {
            'fields': ('phone_number', 'email', 'opening_hours')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__student_id', 'location__name')
    readonly_fields = ('created_at',)
