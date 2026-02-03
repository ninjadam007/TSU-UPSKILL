# ระบุ Path ของ AppConfig เพื่อให้ Django รู้จักตัวตนของแอป Chat อย่างถูกต้อง
default_app_config = 'apps.chat.apps.ChatConfig'

# โน้ต: เราใส่ไว้ตรงนี้เพื่อให้มั่นใจว่าเมื่อ Django เริ่มทำงาน 
# การตั้งค่าทั้งหมดใน apps.py จะถูกดึงไปใช้โดยอัตโนมัติ
