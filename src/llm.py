from google import genai
from PIL import Image
from typing import Optional, Union
import logging
from .config import config

class LLMClient:
    def __init__(self, config: config):
        self.config = config
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.logger = logging.getLogger(__name__)

    def _create_prompt(self, query: str, context: Optional[str] = None) -> str:
        base_prompt = "Bạn là một người hiểu rất rõ về luật pháp của Việt Nam. "
        if context:
            return f"{base_prompt}Hãy dựa vào câu hỏi được cung cấp để trả lời câu hỏi theo luật Việt Nam mới nhất 2025. Nếu không có thông tin để trả lời, hãy nói rõ điều đó. Câu hỏi: {query}. Chỉ đưa thông tin liên quan, không cần lời khuyên và disclaimer"
        return f"{base_prompt}Hãy trả lời câu hỏi sau {query} theo luật Việt Nam mới nhất 2025. Chỉ đưa thông tin liên quan, không cần lời khuyên và disclaimer"

    def ask(self, query: str, context: Optional[str] = None) -> str:
        try:
            prompt = self._create_prompt(query, context)
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            self.logger.error(f"Error in LLM query: {str(e)}")
            return "Xin lỗi, đã có lỗi xảy ra khi xử lý câu hỏi của bạn."

    def process_image(self, image: Union[str, Image.Image]) -> str:
        try:
            if isinstance(image, str):
                image = Image.open(image)
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[image, "Bạn là một người phát hiện những vi phạm về pháp luật. Hãy mô tả ngắn gọn vi phạm trong bức ảnh sau. Chỉ mô tả vi phạm, không cần thông tin thêm"]
            )
            return response.text
        except Exception as e:
            self.logger.error(f"Error processing image: {str(e)}")
            return "Xin lỗi, đã có lỗi xảy ra khi xử lý hình ảnh."

    def process_audio(self, audio_path: str) -> str:
        try:
            raise NotImplementedError("Audio processing not implemented yet")
        except Exception as e:
            self.logger.error(f"Error processing audio: {str(e)}")
            return "Xin lỗi, đã có lỗi xảy ra khi xử lý âm thanh."
