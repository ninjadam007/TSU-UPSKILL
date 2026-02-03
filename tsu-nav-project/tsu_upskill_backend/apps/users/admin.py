from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser, EmailVerificationToken

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # เพิ่มรูปโปรไฟล์ และสถานะสีสันในหน้า List
    list_display = ('profile_tag', 'student_id', 'email', 'full_name_display', 'role_badge', 'is_verified_badge', 'created_at')
    list_filter = ('role', 'is_email_verified', 'is_active')
    search_fields = ('student_id', 'email', 'first_name', 'last_name')
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    actions = ['verify_users', 'make_admin'] # เพิ่มคำสั่งด่วน

    fieldsets = (
        ('บัญชีผู้ใช้', {
            'fields': (('username', 'student_id'), 'password')
        }),
        ('ข้อมูลส่วนตัว', {
            'fields': (('first_name', 'last_name'), 'email', 'phone_number', 'profile_picture')
        }),
        ('ข้อมูลมหาวิทยาลัย (TSU)', {
            'fields': ('department', 'role')
        }),
        ('สถานะและการเข้าถึง', {
            'fields': ('is_email_verified', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('บันทึกเวลา', {
            'fields': ('created_at', 'updated_at', 'last_login'),
            'classes': ('collapse',)
        }),
    )

    # 1. แสดงรูปโปรไฟล์จิ๋ว
    def profile_tag(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="width: 35px; height: 35px; border-radius: 50%; object-fit: cover;" />', obj.profile_picture.url)
        return format_html('<div style="width: 35px; height: 35px; border-radius: 50%; background: #ddd; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #666;">TSU</div>')
    profile_tag.short_description = 'รูป'

    # 2. แสดงชื่อเต็มแบบสวยงาม
    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name_display.short_description = 'ชื่อ-นามสกุล'

    # 3. Badge แสดงบทบาท
    def role_badge(self, obj):
        colors = {'student': '#1890ff', 'staff': '#722ed1', 'admin': '#f5222d'}
        return format_html('<span style="background: {}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px;">{}</span>', 
                           colors.get(obj.role, '#000'), obj.get_role_display())
    role_badge.short_description = 'สิทธิ์'

    # 4. Badge ยืนยันอีเมล
    def is_verified_badge(self, obj):
        if obj.is_email_verified:
            return format_html('<span style="color: #52c41a; font-weight: bold;">✔ Verified</span>')
        return format_html('<span style="color: #faad14;">✘ Unverified</span>')
    is_verified_badge.short_description = 'การยืนยัน'

    # --- Actions (คำสั่งด่วน) ---
    @admin.action(description='ยืนยันอีเมลให้ผู้ใช้ที่เลือก')
    def verify_users(self, request, queryset):
        queryset.update(is_email_verified=True)

    @admin.action(description='ตั้งค่าผู้ใช้ที่เลือกเป็น Admin')
    def make_admin(self, request, queryset):
        queryset.update(role='admin', is_staff=True)

@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token_status', 'created_at', 'expires_at')
    readonly_fields = ('created_at',)

    def token_status(self, obj):
        from django.utils import timezone
        if obj.expires_at < timezone.now():
            return format_html('<span style="color: #ff4d4f;">Expired</span>')
        return format_html('<span style="color: #52c41a;">Active</span>')
    token_status.short_description = 'สถานะ Token'
