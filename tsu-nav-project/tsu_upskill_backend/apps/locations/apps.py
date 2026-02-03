from django.apps import AppConfig

class LocationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.locations'
    
    # ปรับชื่อให้แสดงผลในหน้า Admin เป็นภาษาไทยที่ดูเป็นทางการ
    verbose_name = 'ระบบจัดการสถานที่และพิกัด (Locations)'
