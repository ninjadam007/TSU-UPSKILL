from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, EmailVerificationToken
import re

class UserSerializer(serializers.ModelSerializer):
    """ส่งข้อมูลโปรไฟล์กลับไปแสดงผลที่หน้าบ้าน (React)"""
    class Meta:
        model = CustomUser
        fields = (
            'id', 'student_id', 'username', 'email', 'first_name',
            'last_name', 'phone_number', 'department', 'profile_picture',
            'role', 'is_email_verified', 'created_at'
        )
        read_only_fields = ('id', 'created_at', 'is_email_verified', 'role')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """จัดการสมัครสมาชิกใหม่"""
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = CustomUser
        fields = (
            'student_id', 'email', 'username', 'first_name',
            'last_name', 'password', 'password_confirm'
        )
    
    def validate_email(self, value):
        # ตรวจสอบโดเมนอีเมล
        if not value.endswith('@tsu.ac.th'):
            raise serializers.ValidationError("กรุณาใช้อีเมลมหาวิทยาลัย (@tsu.ac.th)")
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("อีเมลนี้ถูกใช้งานไปแล้ว")
        return value
    
    def validate_student_id(self, value):
        # ตรวจสอบรหัสนิสิต 10 หลัก
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("รหัสนิสิตต้องเป็นตัวเลข 10 หลัก")
        if CustomUser.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("รหัสนิสิตนี้ลงทะเบียนไว้แล้ว")
        return value
    
    def validate(self, data):
        # ตรวจสอบการยืนยันรหัสผ่าน
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "รหัสผ่านไม่ตรงกัน"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        # ใช้ create_user เพื่อให้รหัสผ่านถูก Hashing อัตโนมัติ
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """จัดการการเข้าสู่ระบบด้วยรหัสนิสิต"""
    student_id = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        student_id = data.get('student_id')
        password = data.get('password')
        
        if student_id and password:
            # ค้นหา user จาก student_id
            try:
                user_obj = CustomUser.objects.get(student_id=student_id)
                # ใช้ authenticate เพื่อความปลอดภัยตามมาตรฐาน Django
                user = authenticate(username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                user = None

            if not user:
                raise serializers.ValidationError("รหัสนิสิตหรือรหัสผ่านไม่ถูกต้อง")
            
            if not user.is_active:
                raise serializers.ValidationError("บัญชีนี้ถูกระงับการใช้งาน")
            
            if not user.is_email_verified:
                raise serializers.ValidationError("กรุณายืนยันอีเมลก่อนเข้าสู่ระบบ")
        else:
            raise serializers.ValidationError("กรุณากรอกรหัสนิสิตและรหัสผ่าน")

        data['user'] = user
        return data
