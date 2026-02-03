"""Gemini AI Service Integration - Optimized for TSU UPSKILL"""
import logging
from django.conf import settings
import google.generativeai as genai

logger = logging.getLogger(__name__)

# ตั้งค่า Gemini API
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
else:
    logger.error("❌ GEMINI_API_KEY is missing in settings!")

# ปรับปรุง SYSTEM_PROMPT ให้ชัดเจนและเน้นบริบทของมหาวิทยาลัย
SYSTEM_PROMPT = """คุณคือผู้ช่วยอัจฉริยะ (AI Assistant) ของมหาวิทยาลัยทักษิณ (TSU) ภายใต้โปรเจกต์ TSU UPSKILL
หน้าที่ของคุณคือช่วยเหลือนักศึกษาในการนำทาง ค้นหาสถานที่ และตอบคำถามทั่วไปเกี่ยวกับมหาวิทยาลัย

กฎในการตอบ:
1. ตอบด้วยความเป็นมิตร สุภาพ และเป็นกันเอง (พี่ชาย/น้องสาว/ครับ/ค่ะ)
2. ให้ข้อมูลเส้นทางหรือตำแหน่งที่ชัดเจน
3. หากคุณไม่ทราบคำตอบจริงๆ หรือข้อมูลมีความซับซ้อน ให้ตอบว่า "ขออภัยครับ ข้อมูลส่วนนี้ผมไม่แน่ใจ เพื่อความถูกต้อง ผมขอส่งเรื่องต่อให้แอดมินตรวจสอบให้นะครับ" และส่งค่า True ในระบบ Fallback
4. ตอบสั้น กระชับ เข้าใจง่าย
5. ตอบเป็นภาษาไทยเป็นหลัก เว้นแต่ผู้ใช้จะถามเป็นภาษาอังกฤษ"""

def get_gemini_response(user_message: str, chat_session=None) -> tuple:
    """
    รับคำตอบจาก Google Gemini API พร้อมระบบตรวจจับความไม่แน่ใจ
    Returns:
        tuple: (response_text, is_fallback_to_admin)
    """
    try:
        if not settings.GEMINI_API_KEY:
            logger.warning("⚠️ GEMINI_API_KEY not configured")
            return "ขณะนี้ระบบ AI ยังไม่พร้อมใช้งาน กรุณารอการตอบกลับจากแอดมินครับ", True
        
        # เลือกใช้ model (gemini-1.5-flash หรือ gemini-pro)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # สร้างรายการข้อความเริ่มต้นด้วย SYSTEM_PROMPT
        # หมายเหตุ: สำหรับ Gemini เรามักจะใส่ System instruction ไว้ตอนสร้าง Model 
        # หรือใส่เป็นข้อความแรกของประวัติการคุย
        formatted_messages = [
            {'role': 'user', 'parts': [SYSTEM_PROMPT]},
            {'role': 'model', 'parts': ["รับทราบครับ ผมพร้อมช่วยเหลือสมาชิก TSU UPSKILL ทุกท่านแล้วครับ"]}
        ]
        
        # ดึงประวัติการคุยจาก Database (ถ้ามี)
        if chat_session:
            # ดึง 10 ข้อความล่าสุดเพื่อประหยัด Token และคงบริบท
            db_messages = chat_session.messages.all().order_by('created_at')[:10]
            for msg in db_messages:
                role = 'user' if msg.sender == 'user' else 'model'
                formatted_messages.append({
                    'role': role,
                    'parts': [msg.content]
                })
        
        # เพิ่มคำถามปัจจุบันของผู้ใช้
        formatted_messages.append({
            'role': 'user',
            'parts': [user_message]
        })
        
        # เรียกใช้ Gemini
        try:
            response = model.generate_content(
                contents=formatted_messages,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.9,
                    max_output_tokens=1000,
                ),
                safety_settings=[
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
                ],
            )
            
            ai_response = response.text
            
            # ตรวจสอบว่า AI ลังเลหรือตอบไม่ได้หรือไม่
            if _is_uncertain_response(ai_response):
                return ai_response + "\n\n(ระบบกำลังประสานงานให้แอดมินมาดูแลเพิ่มเติมครับ)", True
            
            return ai_response, False
        
        except Exception as e:
            logger.error(f"❌ Gemini API Execution error: {str(e)}")
            return "ขออภัยครับพี่ชาย ระบบประมวลผลขัดข้องชั่วคราว พี่รอแอดมินสักครู่นะครับ", True
            
    except Exception as e:
        logger.error(f"❌ Unexpected error in get_gemini_response: {str(e)}")
        return "เกิดข้อผิดพลาดไม่คาดคิด กรุณาลองใหม่อีกครั้งหรือติดต่อแอดมินครับ", True


def _is_uncertain_response(response: str) -> bool:
    """เช็ค Keyword ที่บ่งบอกว่า AI ตอบไม่ได้ เพื่อส่งต่อให้แอดมิน"""
    uncertain_keywords = [
        "ไม่ทราบ", 
        "ไม่แน่ใจ", 
        "ไม่มีข้อมูล",
        "i don't know", 
        "not sure", 
        "beyond my knowledge",
        "unable to provide",
        "ขอส่งเรื่องต่อให้แอดมิน",
        "ติดต่อแอดมิน"
    ]
    
    response_lower = response.lower()
    return any(keyword in response_lower for keyword in uncertain_keywords)
