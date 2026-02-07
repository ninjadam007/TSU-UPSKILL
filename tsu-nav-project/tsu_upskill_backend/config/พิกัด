from django.db import models

class LocationCategory(models.Model):
    """หมวดหมู่สถานที่ เช่น อาคารเรียน, สำนักงาน, ห้องอาหาร"""
    name = models.CharField(max_length=100, verbose_name="ชื่อหมวดหมู่")
    icon = models.CharField(max_length=50, help_text="ชื่อ Class ของ FontAwesome เช่น fa-building")

    class Meta:
        verbose_name_plural = "หมวดหมู่สถานที่"

    def __str__(self):
        return self.name

class Location(models.Model):
    """ข้อมูลพิกัดสถานที่จริงใน TSU"""
    name = models.CharField(max_length=200, verbose_name="ชื่อสถานที่")
    category = models.ForeignKey(LocationCategory, on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField(verbose_name="ละติจูด")
    longitude = models.FloatField(verbose_name="ลองจิจูด")
    description = models.TextField(blank=True, verbose_name="รายละเอียด")
    building_code = models.CharField(max_length=20, blank=True, verbose_name="รหัสอาคาร")
    image = models.ImageField(upload_to='locations/', null=True, blank=True, verbose_name="รูปภาพสถานที่")

    class Meta:
        verbose_name_plural = "ข้อมูลพิกัดสถานที่"

    def __str__(self):
        return f"{self.building_code} - {self.name}"
