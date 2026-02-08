from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    
    # ✅ เพิ่มบรรทัดนี้ เพื่อให้ Django อ้างอิงแอปนี้ด้วยคำว่า 'users' ได้อย่างถูกต้อง
    label = 'users' 

    # ชื่อที่แสดงในหน้า Admin (พี่ James แก้ไว้สวยแล้ว ผมคงไว้ให้ครับ)
    verbose_name = 'ระบบจัดการข้อมูลนิสิตและบุคลากร (Users)'

    def ready(self):
        """
        เชื่อมต่อระบบ Signals หากมีการใช้งานในอนาคต
        """
        try:
            import apps.users.signals
        except ImportError:
            pass
