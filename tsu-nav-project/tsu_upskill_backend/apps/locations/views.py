from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from .models import Location, LocationCategory, Bookmark
from .serializers import (
    LocationSerializer, LocationCategorySerializer, BookmarkSerializer
)

class LocationCategoryViewSet(viewsets.ModelViewSet):
    """จัดการหมวดหมู่สถานที่ (ตึกเรียน, โรงอาหาร, ห้องสมุด)"""
    queryset = LocationCategory.objects.all().order_by('name')
    serializer_class = LocationCategorySerializer
    
    def get_permissions(self):
        # ให้ทุกคนดูได้ แต่คนสร้าง/แก้ต้องเป็น Admin เท่านั้น
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class LocationViewSet(viewsets.ModelViewSet):
    """จัดการข้อมูลพิกัดสถานที่และการค้นหา"""
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'building_code']
    search_fields = ['name', 'description', 'building_code', 'room_number']
    ordering_fields = ['name', 'created_at']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_context(self):
        # ส่ง request เข้าไปใน serializer เพื่อให้เช็ค is_bookmarked ได้
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_bookmarks(self, request):
        """ดึงรายการสถานที่ที่นิสิตบันทึกไว้"""
        bookmarks = Bookmark.objects.filter(user=request.user)
        # ใช้ serializer ของ Bookmark เพื่อให้ได้ข้อมูลสถานที่แบบเต็ม
        serializer = BookmarkSerializer(bookmarks, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_bookmark(self, request, pk=None):
        """กดครั้งเดียว: บันทึกถ้ายังไม่มี หรือยกเลิกถ้าบันทึกไว้แล้ว (Smart UX)"""
        location = self.get_object()
        bookmark_query = Bookmark.objects.filter(user=request.user, location=location)
        
        if bookmark_query.exists():
            bookmark_query.delete()
            return Response({'status': 'unbookmarked', 'is_bookmarked': False}, status=status.HTTP_200_OK)
        
        Bookmark.objects.create(user=request.user, location=location)
        return Response({'status': 'bookmarked', 'is_bookmarked': True}, status=status.HTTP_201_CREATED)
