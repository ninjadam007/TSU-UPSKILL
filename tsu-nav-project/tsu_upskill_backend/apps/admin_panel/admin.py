from django.contrib import admin
from django.contrib.auth.models import Group

# ตั้งค่าหัวข้อหน้า Admin ให้เป็นชื่อโครงการ TSU UPSKILL
admin.site.site_header = "TSU UPSKILL Management System"
admin.site.site_title = "TSU Admin Portal"
admin.site.index_title = "ยินดีต้อนรับคุณ James (Admin)"

# โดยปกติแอป admin_panel จะเป็นตัวรวบรวมสถิติ 
# เราจะใช้ไฟล์นี้ในการปรับแต่งหน้าแรกของ Django Admin
# และจัดการสิทธิ์การเข้าถึง (Permissions) ต่างๆ ในอนาคต

# ตัวอย่าง: การซ่อน Group (ถ้าไม่ต้องการให้แอดมินทั่วไปแก้สิทธิ์)
# admin.site.unregister(Group)

# หมายเหตุ: สำหรับ Model หลักๆ เช่น Chat หรือ User 
# เราจะไปลงทะเบียนที่ admin.py ของแอปนั้นๆ เพื่อความเป็นระเบียบครับ
