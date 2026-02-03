from django.apps import AppConfig

class AdminPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.admin_panel'
    
    # ปรับชื่อให้แสดงผลในหน้า Django Admin ให้สวยงามและตรงตามโปรเจกต์
    verbose_name = 'TSU Dashboard & Statistics'

    def ready(self):
        # พื้นที่สำหรับโหลด signals หรือการตั้งค่าเริ่มต้นเมื่อแอปเริ่มทำงาน
        pass
