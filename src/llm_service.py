from google import genai
from PIL import Image
import streamlit as st
from src.config import Config

class LLMService:
    def __init__(self):
        self.config = Config()
        self.client = self.initialize_client()
        
    def initialize_client(_self):
        key = _self.config.GEMINI_API_KEY
        if not key:
            st.warning("Gemini API key not found. Please set your API key in a .env file.")
            return None
            
        try:
            client = genai.Client(api_key=key)
            return client
        except Exception as e:
            st.error(f"Failed to initialize Gemini client: {str(e)}")
            return None
    
    def ask_llm(_self, query, context=""):
        try:
            if context:
                response = _self.client.models.generate_content(
                    model=_self.config.LLM_MODEL,
                    contents=f"Bạn là một người hiểu rất rõ về luật pháp của Việt Nam. Hãy dựa vào câu hỏi và thông tin bổ sung được cung cấp để trả lời vể pháp luật Việt Nam mới nhất 2025. Nếu không có thông tin đủ để trả lời, hãy nói rõ điều đó. Câu hỏi: {query}. Thông tin bổ sung: {context}. Chú ý chỉ đưa thông tin liên quan, không cần lời khuyên và disclaimer"
                )
            else:
                response = _self.client.models.generate_content(
                    model=_self.config.LLM_MODEL,
                    contents=f"Bạn là một người hiểu rất rõ về luật pháp của Việt Nam. Hãy trả lời câu hỏi sau {query} theo luật Việt Nam mới nhất 2025. Chú ý chỉ đưa thông tin liên quan, không cần lời khuyên và disclaimer"
                )
            
            return response.text
        
        except Exception as e:
            return f"Đã xảy ra lỗi khi gọi API: {str(e)}"
    
    def process_image(self, image_file):
        try:
            client = self.client
                
            image = Image.open(image_file)
            response = client.models.generate_content(
                model=self.config.LLM_MODEL,
                contents=[image, "Bạn là một người phát hiện những vi phạm về pháp luật. Hãy mô tả ngắn gọn vi phạm trong bức ảnh sau. Chỉ mô tả vi phạm, không cần thông tin thêm"]
            )
            return response.text
        except Exception as e:
            return f"Đã xảy ra lỗi khi xử lý hình ảnh: {str(e)}"
    
    def process_audio(self, audio_file):
        return "Đây là mẫu kết quả phân tích âm thanh." 
