from rest_framework import serializers
from .models import SystemAnnouncement

class SystemAnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = SystemAnnouncement
        fields = [
            'id', 'title', 'content', 'created_at', 
            'is_active', 'author', 'author_name'
        ]
        read_only_fields = ['created_at', 'author']
