"""Custom authentication classes"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    """Custom JWT authentication"""
    
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is not None:
            user, validated_token = result
            if not user.is_email_verified:
                raise AuthenticationFailed('Email not verified')
        return result
