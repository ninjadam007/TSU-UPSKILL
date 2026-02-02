from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, EmailVerificationToken
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 'student_id', 'username', 'email', 'first_name',
            'last_name', 'phone_number', 'department', 'profile_picture',
            'role', 'is_email_verified', 'created_at'
        )
        read_only_fields = ('id', 'created_at', 'is_email_verified', 'role')


class UserRegistrationSerializer(serializers.ModelSerializer):
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
        """Validate email is @tsu.ac.th"""
        if not value.endswith('@tsu.ac.th'):
            raise serializers.ValidationError(
                "Email must be from @tsu.ac.th domain"
            )
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered")
        return value
    
    def validate_student_id(self, value):
        """Validate student ID is 10 digits"""
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError(
                "Student ID must be exactly 10 digits"
            )
        if CustomUser.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("This student ID is already registered")
        return value
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password': 'Passwords do not match'
            })
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    student_id = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, data):
        student_id = data.get('student_id')
        password = data.get('password')
        
        try:
            user = CustomUser.objects.get(student_id=student_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid student ID or password")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid student ID or password")
        
        if not user.is_email_verified:
            raise serializers.ValidationError("Please verify your email first")
        
        data['user'] = user
        return data
