# ระบุ Default App Config เพื่อให้ Django จัดการ Custom User Model ของ TSU UPSKILL ได้อย่างแม่นยำ
default_app_config = 'apps.users.apps.UsersConfig'

# การเชื่อมต่อตรงนี้สำคัญมาก เพราะแอปอื่นแทบทุกแอป (Chat, Locations, Admin) 
# จะต้องวิ่งมาอ้างอิง User จากแอปนี้เป็นหลักครับ
