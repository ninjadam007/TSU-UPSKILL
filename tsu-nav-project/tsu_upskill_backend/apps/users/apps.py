from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    
    # ปรับชื่อให้แสดงในหน้า Admin เป็นภาษาไทยที่ดูเป็นทางการ
    # ช่วยให้แอดมิน James แยกโซนจัดการ "คน" ออกจากโซน "แชท" ได้ง่ายขึ้น
    verbose_name = 'ระบบจัดการข้อมูลนิสิตและบุคลากร (Users)'

    def ready(self):
        """
        หากในอนาคตมีการทำระบบ Profile อัตโนมัติเมื่อสมัครสมาชิก 
        เราจะนำการ import signals มาไว้ที่นี่ครับ
        """
        try:
            import apps.users.signals
        except ImportError:
            pass
