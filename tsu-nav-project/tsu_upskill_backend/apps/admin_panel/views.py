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
from apps.locations.serializers import LocationSerializer

class AdminDashboardViewSet(viewsets.ViewSet):
    """Admin dashboard statistics and management"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """Get admin dashboard stats"""
        if not request.user.is_admin():
            return Response({
                'error': 'Only admins can access dashboard'
            }, status=status.HTTP_403_FORBIDDEN)
        
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
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def users(self, request):
        """List all users (admin only)"""
        if not request.user.is_admin():
            return Response({
                'error': 'Only admins can view users'
            }, status=status.HTTP_403_FORBIDDEN)
        
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
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def pending_questions(self, request):
        """Get all pending admin questions"""
        if not request.user.is_admin():
            return Response({
                'error': 'Only admins can view pending questions'
            }, status=status.HTTP_403_FORBIDDEN)
        
        pending = PendingAdminQuestion.objects.filter(
            status=PendingAdminQuestion.STATUS_PENDING
        ).order_by('created_at')
        
        serializer = PendingAdminQuestionSerializer(pending, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def respond_to_question(self, request):
        """Admin responds to a pending question"""
        if not request.user.is_admin():
            return Response({
                'error': 'Only admins can respond'
            }, status=status.HTTP_403_FORBIDDEN)
        
        question_id = request.data.get('question_id')
        response_content = request.data.get('response')
        
        try:
            pending = PendingAdminQuestion.objects.get(pk=question_id)
            
            # Create admin response
            admin_msg = Message.objects.create(
                session=pending.message.session,
                sender=Message.SENDER_ADMIN,
                content=response_content,
                admin_user=request.user
            )
            
            # Mark as answered
            pending.status = PendingAdminQuestion.STATUS_ANSWERED
            pending.answered_at = timezone.now()
            pending.save()
            
            return Response({
                'success': True,
                'message': 'Response sent successfully'
            }, status=status.HTTP_200_OK)
        
        except PendingAdminQuestion.DoesNotExist:
            return Response({
                'error': 'Question not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def activity_log(self, request):
        """Get recent activity log"""
        if not request.user.is_admin():
            return Response({
                'error': 'Only admins can view activity log'
            }, status=status.HTTP_403_FORBIDDEN)
        
        recent_messages = Message.objects.select_related(
            'session__user'
        ).order_by('-created_at')[:50]
        
        activity = []
        for msg in recent_messages:
            activity.append({
                'user': msg.session.user.student_id,
                'action': f'Message from {msg.sender}',
                'timestamp': msg.created_at,
                'content': msg.content[:100]
            })
        
        return Response(activity)
