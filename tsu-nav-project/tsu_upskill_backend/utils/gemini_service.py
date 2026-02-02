"""Gemini AI Service Integration"""
import logging
from django.conf import settings
import google.generativeai as genai

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

SYSTEM_PROMPT = """You are a helpful assistant for Thassaksin University (TSU) navigation and campus guidance.
You help students find locations, understand campus directions, and answer general questions about the university.

When answering:
1. Be friendly and helpful
2. Provide clear instructions
3. If you don't know the answer, admit it and suggest asking an admin
4. Keep responses concise and easy to understand
5. Always respond in Thai or English based on the user's language"""

def get_gemini_response(user_message: str, chat_session=None) -> tuple:
    """
    Get response from Google Gemini API
    
    Returns:
        tuple: (response_text, is_fallback_to_admin)
    """
    try:
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not configured")
            return "I'm unable to respond right now. Please wait for admin support.", True
        
        model = genai.GenerativeModel('gemini-pro')
        
        # Build conversation history if session exists
        messages = []
        if chat_session:
            for msg in chat_session.messages.all().order_by('created_at'):
                if msg.sender == 'user':
                    messages.append({
                        'role': 'user',
                        'parts': [msg.content]
                    })
                elif msg.sender == 'ai':
                    messages.append({
                        'role': 'model',
                        'parts': [msg.content]
                    })
        
        # Add current message
        messages.append({
            'role': 'user',
            'parts': [user_message]
        })
        
        # Get response from Gemini
        try:
            response = model.generate_content(
                contents=messages,
                stream=False,
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_DANGEROUS",
                        "threshold": "BLOCK_NONE",
                    },
                ],
            )
            
            ai_response = response.text
            
            # Check if response indicates uncertainty
            if _is_uncertain_response(ai_response):
                return ai_response + "\n\nFor more detailed information, please wait for admin support.", True
            
            return ai_response, False
        
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return "I'm having trouble understanding your question right now. An admin will help you shortly.", True
    
    except Exception as e:
        logger.error(f"Unexpected error in get_gemini_response: {str(e)}")
        return "An error occurred. Please try again or wait for admin support.", True


def _is_uncertain_response(response: str) -> bool:
    """Check if AI response indicates uncertainty"""
    uncertain_keywords = [
        "ไม่ทราบ",  # Thai: "don't know"
        "i don't know",
        "i'm not sure",
        "not certain",
        "unable to",
        "can't answer",
        "beyond my knowledge",
    ]
    
    response_lower = response.lower()
    return any(keyword in response_lower for keyword in uncertain_keywords)
