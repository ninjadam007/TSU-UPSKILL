from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Location, LocationCategory, Bookmark
from .serializers import LocationSerializer, LocationCategorySerializer, BookmarkSerializer

class LocationCategoryViewSet(viewsets.ModelViewSet):
    """Manage location categories"""
    queryset = LocationCategory.objects.all()
    serializer_class = LocationCategorySerializer
    permission_classes = [AllowAny]


class LocationViewSet(viewsets.ModelViewSet):
    """Manage campus locations"""
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description', 'building_code', 'room_number']
    ordering_fields = ['name', 'created_at']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_bookmarks(self, request):
        """Get user's bookmarked locations"""
        bookmarks = Bookmark.objects.filter(user=request.user)
        page = self.paginate_queryset(bookmarks)
        if page is not None:
            serializer = BookmarkSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):
        """Bookmark a location"""
        location = self.get_object()
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            location=location
        )
        
        if created:
            return Response({
                'success': True,
                'message': 'Location bookmarked'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': 'Already bookmarked'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def unbookmark(self, request, pk=None):
        """Remove bookmark from location"""
        location = self.get_object()
        deleted, _ = Bookmark.objects.filter(
            user=request.user,
            location=location
        ).delete()
        
        if deleted:
            return Response({
                'success': True,
                'message': 'Bookmark removed'
            }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                'success': False,
                'message': 'Not bookmarked'
            }, status=status.HTTP_400_BAD_REQUEST)
