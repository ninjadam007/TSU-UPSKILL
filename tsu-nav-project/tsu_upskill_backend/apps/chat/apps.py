from django.apps import AppConfig

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.chat'
    verbose_name = 'ระบบแชทอัจฉริยะ (AI Chat)' # เปลี่ยนชื่อให้ดูดีในหน้า Admin

    def ready(self):
        # ตรงนี้สามารถใส่การ import signals ได้ถ้าพี่ต้องการให้ระบบ
        # ทำงานอัตโนมัติเมื่อมีการส่งข้อความ
        import apps.chat.signals  # ถ้ามีไฟล์ signals.py
