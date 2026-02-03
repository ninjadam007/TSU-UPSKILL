# เชื่อมต่อ AppConfig เพื่อให้ Django รู้จักแอป Locations อย่างเป็นทางการ
default_app_config = 'apps.locations.apps.LocationsConfig'

# โน้ต: การระบุไว้ตรงนี้ช่วยป้องกัน Error เวลาเราย้ายแอปไปไว้ในโฟลเดอร์ย่อย (เช่น apps/)
# และช่วยให้ระบบค้นหาพิกัดสถานที่ทำงานได้อย่างถูกต้องตั้งแต่เริ่มต้น Server
