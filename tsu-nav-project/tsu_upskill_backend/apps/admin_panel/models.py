from django.db import models
from django.conf import settings

class SystemAnnouncement(models.Model):
    """โมเดลสำหรับประกาศข่าวสารจากแอดมินไปยังหน้า Dashboard ของนักศึกษา"""
    title = models.CharField(max_length=255, verbose_name="หัวข้อประกาศ")
    content = models.TextField(verbose_name="เนื้อหาประกาศ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="สร้างเมื่อ")
    is_active = models.BooleanField(default=True, verbose_name="กำลังใช้งาน")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,  # ✅ แก้ไขจาก on_ Harris เป็น on_delete
        verbose_name="ผู้ประกาศ"
    )

    class Meta:
        verbose_name = "ประกาศระบบ"
        verbose_name_plural = "ประกาศระบบ"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
