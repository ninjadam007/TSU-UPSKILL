from rest_framework import serializers
from .models import Location, LocationCategory, Bookmark

class LocationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCategory
        fields = ('id', 'name', 'description', 'icon')


class LocationSerializer(serializers.ModelSerializer):
    category = LocationCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)
    is_bookmarked = serializers.SerializerMethodField()
    
    class Meta:
        model = Location
        fields = (
            'id', 'name', 'category', 'category_id', 'description',
            'latitude', 'longitude', 'building_code', 'floor', 'room_number',
            'image', 'opening_hours', 'phone_number', 'email', 'is_active',
            'is_bookmarked', 'created_at'
        )
        read_only_fields = ('id', 'created_at', 'is_bookmarked')
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Bookmark.objects.filter(
                user=request.user,
                location=obj
            ).exists()
        return False


class BookmarkSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    location_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Bookmark
        fields = ('id', 'location', 'location_id', 'created_at')
        read_only_fields = ('id', 'created_at')
