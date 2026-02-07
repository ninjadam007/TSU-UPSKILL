"""
URL Configuration for TSU UPSKILL Backend
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

# ฟังก์ชันหน้าแรกเพื่อความสะดวกในการเช็กสถานะ
def api_root_view(request):
    return JsonResponse({
        "project": "TSU UPSKILL API",
        "status": "online",
        "endpoints": {
            "auth": "/api/users/auth/",
            "locations": "/api/locations/",
            "chat": "/api/chat/",
            "admin": "/admin/"
        }
    })

urlpatterns = [
    path('', api_root_view, name='api-root'), 
    path('admin/', admin.site.urls),
    
    # ดึง URLs จากแต่ละแอปเข้ามา
    # หมายเหตุ: ผมใส่ Prefix แยกตามแอปเพื่อให้จัดการง่ายและไม่สับสนครับ
    path('api/users/', include('apps.users.urls')),
    path('api/locations/', include('apps.locations.urls')),
    path('api/chat/', include('apps.chat.urls')),
    path('api/admin-panel/', include('apps.admin_panel.urls')),
]

# จัดการไฟล์รูปภาพและไฟล์ Static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# แต่งหน้า Admin ให้เป็นแบรนด์ TSU
admin.site.site_header = "TSU UPSKILL Admin"
admin.site.site_title = "TSU UPSKILL"
admin.site.index_title = "จัดการระบบ TSU UPSKILL"
