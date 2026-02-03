from rest_framework import serializers
from .models import ChatSession, Message, PendingAdminQuestion

class MessageSerializer(serializers.ModelSerializer):
    # ดึงชื่อแอดมินมาแสดงถ้ามีการตอบกลับ
    admin_user_name = serializers.CharField(
        source='admin_user.get_full_name',
        read_only=True,
        default=None
    )
    
    class Meta:
        model = Message
        fields = (
            'id', 'sender', 'content', 'is_fallback_to_admin',
            'admin_user_name', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class ChatSessionSerializer(serializers.ModelSerializer):
    # ดึงข้อความทั้งหมดในเซสชันนั้นมาด้วย (สำหรับหน้าแชท)
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.IntegerField(source='messages.count', read_only=True)
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = (
            'id', 'title', 'created_at', 'updated_at',
            'message_count', 'last_message', 'messages'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_last_message(self, obj):
        # ดึงข้อความล่าสุดไปโชว์ในหน้า Sidebar ของ React
        last_msg = obj.messages.order_by('-created_at').first()
        if last_msg:
            return {
                'content': last_msg.content[:50] + "..." if len(last_msg.content) > 50 else last_msg.content,
                'sender': last_msg.sender,
                'created_at': last_msg.created_at
            }
        return None


class SendMessageSerializer(serializers.Serializer):
    # รับค่าจากหน้าบ้านเวลาเด็กกดส่งข้อความ
    content = serializers.CharField(max_length=2000, required=True)
    session_id = serializers.IntegerField(required=False)


class PendingAdminQuestionSerializer(serializers.ModelSerializer):
    message_content = serializers.CharField(source='message.content', read_only=True)
    student_id = serializers.CharField(source='message.session.user.student_id', read_only=True)
    user_name = serializers.CharField(source='message.session.user.get_full_name', read_only=True)
    
    class Meta:
        model = PendingAdminQuestion
        fields = (
            'id', 'message_content', 'student_id', 'user_name', 
            'status', 'created_at', 'answered_at'
        )
        read_only_fields = ('id', 'created_at', 'answered_at')
