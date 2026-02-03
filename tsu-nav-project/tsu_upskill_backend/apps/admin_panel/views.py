from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q

from apps.users.models import CustomUser
from apps.users.serializers import UserSerializer
from apps.chat.models import PendingAdminQuestion, Message
from apps.chat.serializers import PendingAdminQuestionSerializer, MessageSerializer
from apps.locations.models import Location
from .models import SystemAnnouncement  # เพิ่มโมเดลประกาศ
from .serializers import SystemAnnouncementSerializer # (ต้องสร้างในไฟล์ถัดไป)

class AdminDashboardViewSet(viewsets.ViewSet):
    """ระบบหลังบ้านสำหรับแอดมิน: ดูสถิติ จัดการผู้ใช้ และตอบคำถาม"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """ดึงข้อมูลสถิติรวมของระบบ TSU UPSKILL"""
        if not request.user.is_admin():
            return Response({'error': 'สิทธิ์เข้าถึงเฉพาะแอดมินเท่านั้น'}, status=status.HTTP_403_FORBIDDEN)
        
        stats = {
            'total_users': CustomUser.objects.filter(role=CustomUser.STUDENT).count(),
            'pending_questions': PendingAdminQuestion.objects.filter(
                status=PendingAdminQuestion.STATUS_PENDING
            ).count(),
            'total_locations': Location.objects.filter(is_active=True).count(),
            'verified_users': CustomUser.objects.filter(
                role=CustomUser.STUDENT,
                is_email_verified=True
            ).count(),
            'active_announcements': SystemAnnouncement.objects.filter(is_active=True).count()
        }
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def users(self, request):
        """รายชื่อนิสิตทั้งหมด พร้อมระบบค้นหา"""
        if not request.user.is_admin():
            return Response({'error': 'สิทธิ์ไม่ถึงครับพี่ชาย'}, status=status.HTTP_403_FORBIDDEN)
        
        users = CustomUser.objects.filter(role=CustomUser.STUDENT)
        search = request.query_params.get('search')
        if search:
            users = users.filter(
                Q(student_id__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search)
            )
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def respond_to_question(self, request):
        """แอดมินตอบคำถามนิสิต และปิดสถานะ Pending"""
        if not request.user.is_admin():
            return Response({'error': 'เฉพาะแอดมิน James เท่านั้นที่ตอบได้'}, status=status.HTTP_403_FORBIDDEN)
        
        question_id = request.data.get('question_id')
        response_content = request.data.get('response')
        
        try:
            pending = PendingAdminQuestion.objects.get(pk=question_id)
            
            # สร้างข้อความตอบกลับจากแอดมิน
            Message.objects.create(
                session=pending.message.session,
                sender=Message.SENDER_ADMIN,
                content=response_content,
                admin_user=request.user
            )
            
            # อัปเดตสถานะคำถาม
            pending.status = PendingAdminQuestion.STATUS_ANSWERED
            pending.answered_at = timezone.now()
            pending.save()
            
            return Response({'success': True, 'message': 'ส่งคำตอบเรียบร้อยแล้ว'}, status=status.HTTP_200_OK)
        except PendingAdminQuestion.DoesNotExist:
            return Response({'error': 'ไม่พบคำถามนี้ในระบบ'}, status=status.HTTP_404_NOT_FOUND)

class AnnouncementViewSet(viewsets.ModelViewSet):
    """จัดการประกาศข่าวสาร (CRUD)"""
    queryset = SystemAnnouncement.objects.all()
    serializer_class = SystemAnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # ถ้านิสิตดู จะเห็นแค่ที่เปิดใช้งานอยู่ ถ้าแอดมินจะเห็นทั้งหมด
        if self.request.user.is_admin():
            return SystemAnnouncement.objects.all()
        return SystemAnnouncement.objects.filter(is_active=True)
