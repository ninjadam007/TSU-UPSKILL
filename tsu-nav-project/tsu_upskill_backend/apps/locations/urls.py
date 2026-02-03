from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, LocationCategoryViewSet

# สร้าง Router สำหรับจัดการ Endpoints อัตโนมัติ
router = DefaultRouter()

# /api/locations/locations/ -> จัดการข้อมูลสถานที่และการค้นหา
router.register(r'locations', LocationViewSet, basename='location')

# /api/locations/categories/ -> จัดการหมวดหมู่ (ตึก, ห้องสมุด, โรงอาหาร)
router.register(r'categories', LocationCategoryViewSet, basename='location-category')

urlpatterns = [
    # รวมเส้นทางจาก Router เข้ามา
    path('', include(router.urls)),
]
