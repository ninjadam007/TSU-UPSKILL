from django.contrib import admin
from .models import Message, PendingAdminQuestion

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # แก้ (E108): เอา 'get_user' ออก แล้วใช้ 'sender' หรือ 'content' แทน
    list_display = ('id', 'sender', 'content', 'created_at')
    list_filter = ('sender', 'created_at')

@admin.register(PendingAdminQuestion)
class PendingAdminQuestionAdmin(admin.ModelAdmin):
    # แก้ (E108) และ (E122):
    # 1. เอา 'get_user' ออก
    # 2. ต้องมี 'status' ใน list_display ถึงจะใช้ใน list_editable ได้
    list_display = ('id', 'status', 'created_at', 'answered_at')
    list_editable = ('status',) 
    list_filter = ('status', 'created_at')
