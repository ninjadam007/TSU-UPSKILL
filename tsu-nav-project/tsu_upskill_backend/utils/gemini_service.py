"""Gemini AI Service Integration - Optimized for TSU UPSKILL"""
import logging
from django.conf import settings
import google.generativeai as genai

logger = logging.getLogger(__name__)

# ย้าย SYSTEM_PROMPT ไว้ข้างนอกได้เพราะเป็นแค่ String (ไม่กินแรม)
SYSTEM_PROMPT = """คุณคือผู้ช่วยอัจฉริยะ (AI Assistant) ของมหาวิทยาลัยทักษิณ (TSU) ภายใต้โปรเจกต์ TSU UPSKILL
หน้าที่ของคุณคือช่วยเหลือนักศึกษาในการนำทาง ค้นหาสถานที่ และตอบคำถามทั่วไปเกี่ยวกับมหาวิทยาลัย..."""

def get_gemini_response(user_message: str, chat_session=None) -> tuple:
    try:
        if not settings.GEMINI_API_KEY:
            logger.warning("⚠️ GEMINI_API_KEY not configured")
            return "ขณะนี้ระบบ AI ยังไม่พร้อมใช้งาน กรุณารอการตอบกลับจากแอดมินครับ", True
        
        # ✅ แก้ไข: ตั้งค่า API เฉพาะตอนที่จะใช้งาน (Lazy Loading)
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # สร้างรายการข้อความ (Context)
        formatted_messages = [
            {'role': 'user', 'parts': [SYSTEM_PROMPT]},
            {'role': 'model', 'parts': ["รับทราบครับ ผมพร้อมช่วยเหลือสมาชิก TSU UPSKILL แล้วครับ"]}
        ]
        
        if chat_session:
            db_messages = chat_session.messages.all().order_by('created_at')[:10]
            for msg in db_messages:
                role = 'user' if msg.sender == 'user' else 'model'
                formatted_messages.append({'role': role, 'parts': [msg.content]})
        
        formatted_messages.append({'role': 'user', 'parts': [user_message]})
        
        # เรียกใช้ Gemini
        response = model.generate_content(
            contents=formatted_messages,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.9,
                max_output_tokens=1000,
            )
        )
        
        ai_response = response.text
        if _is_uncertain_response(ai_response):
            return ai_response + "\n\n(ระบบกำลังประสานงานให้แอดมินดูแลครับ)", True
            
        return ai_response, False
        
    except Exception as e:
        logger.error(f"❌ Gemini API Error: {str(e)}")
        return "ขออภัยครับ ระบบประมวลผลขัดข้องชั่วคราว พี่รอแอดมินสักครู่นะครับ", True

def _is_uncertain_response(response: str) -> bool:
    uncertain_keywords = ["ไม่ทราบ", "ไม่แน่ใจ", "ไม่มีข้อมูล", "ติดต่อแอดมิน"]
    return any(keyword in response.lower() for keyword in uncertain_keywords)
