from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction

from .models import ChatSession, Message, PendingAdminQuestion
from .serializers import (
    ChatSessionSerializer, MessageSerializer,
    SendMessageSerializer, PendingAdminQuestionSerializer
)

# ✅ แก้ไข: ชี้ไปที่โฟลเดอร์ utils นอกแอปตามโครงสร้างจริงของพี่ James
from utils.gemini_service import get_gemini_response

class ChatSessionViewSet(viewsets.ModelViewSet):
    """ระบบจัดการ Session การแชทสำหรับนิสิต TSU UPSKILL"""
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).order_by('-updated_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """ส่งข้อความไปหา AI และรอรับคำตอบ"""
        session = self.get_object()
        serializer = SendMessageSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_content = serializer.validated_data['content']

        with transaction.atomic():
            # 1. บันทึกข้อความนิสิต
            user_msg = Message.objects.create(
                session=session,
                sender=Message.SENDER_USER,
                content=user_content
            )
            
            # 2. เรียกใช้ Gemini จาก utils
            ai_response, is_fallback = get_gemini_response(user_content, session)
            
            # 3. บันทึกข้อความจาก AI
            ai_msg = Message.objects.create(
                session=session,
                sender=Message.SENDER_AI,
                content=ai_response,
                is_fallback_to_admin=is_fallback
            )
            
            # 4. ถ้า AI ตอบไม่ได้ ให้ส่งเรื่องต่อให้แอดมิน
            if is_fallback:
                PendingAdminQuestion.objects.get_or_create(message=ai_msg)
            
            # 5. ตั้งชื่อแชทให้อัตโนมัติจากข้อความแรก
            if session.messages.count() <= 2:
                session.title = user_content[:50]
                session.save()

        return Response({
            'success': True,
            'messages': MessageSerializer([user_msg, ai_msg], many=True).data,
            'is_fallback': is_fallback
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        session = self.get_object()
        messages = session.messages.all().order_by('created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class PendingAdminQuestionViewSet(viewsets.ViewSet):
    """ส่วนของแอดมินสำหรับจัดการคำถามที่ AI ตอบไม่ได้"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        # ตรวจสอบว่าเป็น Admin หรือ Staff
        if not (request.user.is_staff or (hasattr(request.user, 'is_admin') and request.user.is_admin())):
            return Response({'error': 'เฉพาะแอดมินเท่านั้นครับ'}, status=status.HTTP_403_FORBIDDEN)
        
        pending = PendingAdminQuestion.objects.filter(
            status=PendingAdminQuestion.STATUS_PENDING
        ).order_by('-created_at')
        serializer = PendingAdminQuestionSerializer(pending, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        """แอดมินพิมพ์ตอบคำถาม"""
        if not (request.user.is_staff or (hasattr(request.user, 'is_admin') and request.user.is_admin())):
            return Response({'error': 'สิทธิ์ไม่เพียงพอ'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            pending = PendingAdminQuestion.objects.get(pk=pk)
            response_content = request.data.get('response')

            if not response_content:
                return Response({'error': 'กรุณาใส่ข้อความตอบกลับ'}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                admin_msg = Message.objects.create(
                    session=pending.message.session,
                    sender=Message.SENDER_ADMIN,
                    content=response_content,
                    admin_user=request.user
                )
                pending.status = PendingAdminQuestion.STATUS_ANSWERED
                pending.answered_at = timezone.now()
                pending.save()
            
            return Response({
                'success': True,
                'message': MessageSerializer(admin_msg).data
            }, status=status.HTTP_200_OK)
            
        except PendingAdminQuestion.DoesNotExist:
            return Response({'error': 'ไม่พบรายการนี้'}, status=status.HTTP_404_NOT_FOUND)
