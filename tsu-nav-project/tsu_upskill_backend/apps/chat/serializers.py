from rest_framework import serializers
from .models import ChatSession, Message, PendingAdminQuestion

class MessageSerializer(serializers.ModelSerializer):
    admin_user_name = serializers.CharField(
        source='admin_user.get_full_name',
        read_only=True
    )
    
    class Meta:
        model = Message
        fields = (
            'id', 'sender', 'content', 'is_fallback_to_admin',
            'admin_user_name', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = (
            'id', 'title', 'created_at', 'updated_at',
            'message_count', 'last_message', 'messages'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_message_count(self, obj):
        return obj.messages.count()
    
    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None


class SendMessageSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=2000)
    session_id = serializers.IntegerField(required=False)


class PendingAdminQuestionSerializer(serializers.ModelSerializer):
    message = MessageSerializer(read_only=True)
    user_name = serializers.CharField(
        source='message.session.user.get_full_name',
        read_only=True
    )
    user_email = serializers.CharField(
        source='message.session.user.email',
        read_only=True
    )
    
    class Meta:
        model = PendingAdminQuestion
        fields = (
            'id', 'message', 'user_name', 'user_email',
            'status', 'created_at', 'answered_at'
        )
        read_only_fields = ('id', 'created_at')
