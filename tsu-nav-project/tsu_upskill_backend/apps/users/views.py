from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from datetime import timedelta
import secrets

from .models import CustomUser, EmailVerificationToken
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer
from utils.email_service import send_verification_email

class UserViewSet(viewsets.ViewSet):
    """ศูนย์รวมระบบจัดการสมาชิกและยืนยันตัวตน"""

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """สมัครสมาชิก: สร้าง User และส่ง Email ยืนยัน"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # สร้าง Secure Token อายุ 24 ชม.
            token = secrets.token_urlsafe(50)
            EmailVerificationToken.objects.create(
                user=user,
                token=token,
                expires_at=timezone.now() + timedelta(hours=24)
            )
            
            # ส่งอีเมลหาชาว TSU (เรียกใช้ Service จาก utils)
            send_verification_email(user.email, token)
            
            return Response({
                'success': True,
                'message': 'ลงทะเบียนสำเร็จ! กรุณาตรวจสอบอีเมล @tsu.ac.th เพื่อยืนยันตัวตน',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        """ยืนยันอีเมลด้วย Token ที่ส่งไป"""
        token = request.data.get('token')
        try:
            verification = EmailVerificationToken.objects.get(token=token)
            
            if verification.expires_at < timezone.now():
                verification.delete()
                return Response({'success': False, 'message': 'ขออภัย Token หมดอายุแล้ว'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = verification.user
            user.is_email_verified = True
            user.save()
            verification.delete()
            
            return Response({'success': True, 'message': 'ยืนยันอีเมลสำเร็จ! เข้าสู่ระบบได้เลย'}, status=status.HTTP_200_OK)
        except EmailVerificationToken.DoesNotExist:
            return Response({'success': False, 'message': 'Token ไม่ถูกต้อง'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """เข้าสู่ระบบและออกตั๋ว JWT (SimpleJWT)"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'success': True,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'put'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """ดูโปรไฟล์หรืออัปเดตข้อมูลตัวเองใน Action เดียว"""
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        
        # กรณี PUT (Update Profile)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """เปลี่ยนรหัสผ่าน (พร้อมตรวจสอบความปลอดภัย)"""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response({'success': False, 'message': 'รหัสผ่านเดิมไม่ถูกต้อง'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(new_password) < 8:
            return Response({'success': False, 'message': 'รหัสผ่านใหม่ต้องยาว 8 ตัวขึ้นไป'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'success': True, 'message': 'เปลี่ยนรหัสผ่านสำเร็จแล้ว'})
