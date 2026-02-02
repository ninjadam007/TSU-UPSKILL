"""
URL Configuration for TSU UPSKILL Backend
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

# ฟังก์ชันหน้าแรก (ช่วยให้เช็กสถานะ Server ได้ง่ายขึ้น)
def api_root_view(request):
    return JsonResponse({
        "project": "TSU UPSKILL API",
        "status": "online",
        "admin_panel": "/admin/"
    })

urlpatterns = [
    path('', api_root_view), 
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.locations.urls')),
    path('api/', include('apps.chat.urls')),
    path('api/', include('apps.admin_panel.urls')),
]

# โหลดไฟล์ Media/Static เฉพาะตอนเปิด DEBUG (บนเครื่องตัวเอง)
# บน Render ตัว Whitenoise จะจัดการ Static ให้เองผ่าน Middleware ครับ
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin customization
admin.site.site_header = "TSU UPSKILL Admin"
admin.site.site_title = "TSU UPSKILL"
admin.site.index_title = "Welcome to TSU UPSKILL Administration"
