"""Email Service"""
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

logger = logging.getLogger(__name__)

def send_verification_email(email: str, token: str, domain: str = "localhost:8000"):
    """Send email verification link"""
    try:
        verification_link = f"http://{domain}/api/auth/verify-email/?token={token}"
        
        subject = "TSU UPSKILL - Verify Your Email"
        message = f"""
Hello,

Thank you for registering with TSU UPSKILL!

Please verify your email by clicking the link below:
{verification_link}

This link will expire in 24 hours.

If you didn't create this account, please ignore this email.

Best regards,
TSU UPSKILL Team
        """
        
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Welcome to TSU UPSKILL!</h2>
                <p>Thank you for registering. Please verify your email by clicking the button below:</p>
                <p><a href="{verification_link}" style="background-color: #1e88e5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
                <p>This link will expire in 24 hours.</p>
                <p>If you didn't create this account, please ignore this email.</p>
                <p>Best regards,<br>TSU UPSKILL Team</p>
            </body>
        </html>
        """
        
        send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"Verification email sent to {email}")
    
    except Exception as e:
        logger.error(f"Failed to send verification email to {email}: {str(e)}")


def send_admin_notification(question_content: str, student_email: str, student_name: str):
    """Notify admin about new unanswered question"""
    try:
        subject = "TSU UPSKILL - New Question Needs Response"
        message = f"""
A student has asked a question that AI couldn't answer:

Student: {student_name} ({student_email})
Question: {question_content}

Please log in to the admin panel to respond.
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )
        logger.info(f"Admin notification sent for new question from {student_email}")
    
    except Exception as e:
        logger.error(f"Failed to send admin notification: {str(e)}")


def send_response_notification(student_email: str, response_content: str, admin_name: str):
    """Notify student that admin responded to their question"""
    try:
        subject = "TSU UPSKILL - Your Question Has Been Answered"
        message = f"""
Your question on TSU UPSKILL has been answered!

Response from {admin_name}:
{response_content}

Please log in to check the full conversation.
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student_email],
            fail_silently=True,
        )
        logger.info(f"Response notification sent to {student_email}")
    
    except Exception as e:
        logger.error(f"Failed to send response notification: {str(e)}")
