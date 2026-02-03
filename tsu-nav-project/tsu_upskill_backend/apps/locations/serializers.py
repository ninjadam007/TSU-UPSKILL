from rest_framework import serializers
from .models import Location, LocationCategory, Bookmark

class LocationCategorySerializer(serializers.ModelSerializer):
    # นับจำนวนสถานที่ในหมวดนี้ให้ด้วย (เผื่อไปโชว์ในหน้าค้นหา)
    location_count = serializers.IntegerField(source='locations.count', read_only=True)

    class Meta:
        model = LocationCategory
        fields = ('id', 'name', 'description', 'icon', 'location_count')


class LocationSerializer(serializers.ModelSerializer):
    category = LocationCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=LocationCategory.objects.all(), 
        source='category', 
        write_only=True, 
        required=False
    )
    is_bookmarked = serializers.SerializerMethodField()
    # เพิ่ม URL แผนที่โดยตรงเพื่อให้ AI หรือหน้าบ้านนำไปใช้ได้เลย
    map_url = serializers.ReadOnlyField(source='google_maps_url')

    class Meta:
        model = Location
        fields = (
            'id', 'name', 'category', 'category_id', 'description',
            'latitude', 'longitude', 'map_url', 'building_code', 'floor', 
            'room_number', 'image', 'opening_hours', 'phone_number', 
            'email', 'is_active', 'is_bookmarked', 'created_at'
        )
        read_only_fields = ('id', 'created_at', 'is_bookmarked')

    def get_is_bookmarked(self, obj):
        # ตรวจสอบว่านิสิตคนนี้บันทึกสถานที่นี้ไว้หรือยัง
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # ใช้พารามิเตอร์ของ user จาก request context
            return Bookmark.objects.filter(
                user=request.user,
                location=obj
            ).exists()
        return False


class BookmarkSerializer(serializers.ModelSerializer):
    # ดึงข้อมูลสถานที่แบบเต็มมาโชว์ในหน้า "รายการที่บันทึกไว้"
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), 
        source='location', 
        write_only=True
    )

    class Meta:
        model = Bookmark
        fields = ('id', 'location', 'location_id', 'created_at')
        read_only_fields = ('id', 'created_at')
