from django.apps import AppConfig

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.chat'
    
    # ชื่อที่จะแสดงในหน้า Admin (TSU Theme)
    verbose_name = 'TSU AI Assistant & Chat'

    def ready(self):
        """
        ฟังก์ชันนี้จะทำงานเมื่อ Django เริ่มต้นระบบ 
        เหมาะสำหรับการเชื่อมต่อ Signals เพื่อให้ระบบทำงานอัตโนมัติ
        """
        try:
            import apps.chat.signals  # เชื่อมต่อระบบแจ้งเตือนและประมวลผลอัตโนมัติ
        except ImportError:
            # กันเหนียวไว้เผื่อพี่ยังไม่ได้สร้างไฟล์ signals.py ระบบจะได้ไม่ล่ม
            pass
