from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import ChatSession, Message, PendingAdminQuestion
from .serializers import (
    ChatSessionSerializer, MessageSerializer,
    SendMessageSerializer, PendingAdminQuestionSerializer
)
from utils.gemini_service import get_gemini_response

class ChatSessionViewSet(viewsets.ModelViewSet):
    """Chat session management"""
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Create a new chat session"""
        session = ChatSession.objects.create(user=request.user)
        serializer = self.get_serializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def send_message(self, request, pk=None):
        """Send a message to the AI"""
        session = self.get_object()
        serializer = SendMessageSerializer(data=request.data)
        
        if serializer.is_valid():
            user_message = serializer.validated_data['content']
            
            # Save user message
            user_msg = Message.objects.create(
                session=session,
                sender=Message.SENDER_USER,
                content=user_message
            )
            
            # Get AI response
            ai_response, is_fallback = get_gemini_response(user_message, session)
            
            # Save AI message
            ai_msg = Message.objects.create(
                session=session,
                sender=Message.SENDER_AI,
                content=ai_response,
                is_fallback_to_admin=is_fallback
            )
            
            # If fallback, create pending question for admin
            if is_fallback:
                PendingAdminQuestion.objects.create(message=ai_msg)
            
            # Update session title if it's the first message
            if session.messages.count() == 2:  # user + ai message
                session.title = user_message[:50]
                session.save()
            
            return Response({
                'success': True,
                'messages': MessageSerializer([user_msg, ai_msg], many=True).data,
                'is_fallback': is_fallback
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def messages(self, request, pk=None):
        """Get all messages in a session"""
        session = self.get_object()
        messages = session.messages.all()
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class PendingAdminQuestionViewSet(viewsets.ViewSet):
    """Admin view for pending questions"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """List all pending questions (admin only)"""
        if not request.user.is_admin():
            return Response({
                'error': 'Only admins can view pending questions'
            }, status=status.HTTP_403_FORBIDDEN)
        
        pending = PendingAdminQuestion.objects.filter(
            status=PendingAdminQuestion.STATUS_PENDING
        )
        serializer = PendingAdminQuestionSerializer(pending, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def respond(self, request, pk=None):
        """Admin responds to a pending question"""
        if not request.user.is_admin():
            return Response({
                'error': 'Only admins can respond to questions'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            pending = PendingAdminQuestion.objects.get(pk=pk)
            response_content = request.data.get('response')
            
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
                'message': MessageSerializer(admin_msg).data
            }, status=status.HTTP_200_OK)
        
        except PendingAdminQuestion.DoesNotExist:
            return Response({
                'error': 'Question not found'
            }, status=status.HTTP_404_NOT_FOUND)
