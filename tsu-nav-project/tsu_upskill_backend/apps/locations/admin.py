from django.contrib import admin
from django.utils.html import format_html
from .models import Location, LocationCategory, Bookmark

@admin.register(LocationCategory)
class LocationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_display')
    search_fields = ('name',)

    def icon_display(self, obj):
        return obj.icon if obj.icon else "-"
    icon_display.short_description = 'ไอคอน'

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    # เพิ่มการแสดงรูปภาพจิ๋วและลิงก์แผนที่ในหน้าลิสต์
    list_display = ('image_tag', 'name', 'category', 'building_code', 'is_active', 'map_link')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'building_code', 'room_number')
    readonly_fields = ('image_tag_large', 'created_at', 'updated_at')
    
    fieldsets = (
        ('ข้อมูลทั่วไป', {
            'fields': ('name', 'category', 'description', 'image', 'image_tag_large')
        }),
        ('รายละเอียดสถานที่/อาคาร', {
            'fields': ('building_code', 'floor', 'room_number', ('latitude', 'longitude'))
        }),
        ('การติดต่อและเวลาทำการ', {
            'fields': ('phone_number', 'email', 'opening_hours')
        }),
        ('สถานะระบบ', {
            'fields': ('is_active',)
        }),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height: 45px; border-radius: 5px; object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_tag.short_description = 'รูป'

    def image_tag_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 300px; border-radius: 10px;" />', obj.image.url)
        return "ยังไม่ได้อัปโหลดรูปภาพ"
    image_tag_large.short_description = 'ตัวอย่างรูปขยาย'

    def map_link(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html('<a href="{}" target="_blank" style="color: #1890ff; font-weight: bold;">📍 ดูแผนที่</a>', url)
        return "ไม่มีพิกัด"
    map_link.short_description = 'พิกัด'

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'location', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__student_id', 'location__name')
    
    def user_display(self, obj):
        return f"{obj.user.student_id} ({obj.user.get_full_name()})"
    user_display.short_description = 'นิสิต'
