import pandas as pd
import numpy as np
import torch
import os
import faiss
import streamlit as st
from FlagEmbedding import BGEM3FlagModel
from openai import OpenAI
import Image
from config import config
from google import genai


class LLM:    
    def __init__(self, api_key=None):
        self.api_key = api_key if api_key else config.GEMINI_API_KEY
        self.client = genai.Client(api_key=self.api_key)
        
    def ask_llm(self, query, context=""):
        try:
            base_prompt = "Bạn là một người hiểu rất rõ về luật pháp của Việt Nam. "
            
            if context:
                prompt = (
                    f"{base_prompt}Hãy dựa vào câu hỏi được cung cấp để trả lời câu hỏi "
                    f"theo luật Việt Nam mới nhất 2025. Nếu không có thông tin đủ để trả lời, "
                    f"hãy nói rõ điều đó. Câu hỏi: {query}. Chú ý chỉ đưa thông tin liên quan, "
                    f"không cần lời khuyên và disclaimer"
                )
            else:
                prompt = (
                    f"{base_prompt}Hãy trả lời câu hỏi sau {query} theo luật Việt Nam mới nhất 2025. "
                    f"Chú ý chỉ đưa thông tin liên quan, không cần lời khuyên và disclaimer"
                )
            
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            
            return response.text
        
        except Exception as e:
            return f"Đã xảy ra lỗi khi gọi API: {str(e)}"
    
    def process_image(self, image_file):
        try:
            # Handle both file objects and path strings
            if isinstance(image_file, str):
                image = Image.open(image_file)
            else:
                image = Image.open(image_file)
                
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    image, 
                    "Bạn là một người phát hiện những vi phạm về pháp luật. "
                    "Hãy mô tả ngắn gọn vi phạm trong bức ảnh sau. "
                    "Chỉ mô tả vi phạm, không cần thông tin thêm"
                ]
            )
            
            return response.text
            
        except Exception as e:
            return f"Đã xảy ra lỗi khi xử lý hình ảnh: {str(e)}"
    
    def process_audio(self, audio_file):
        """Process an audio file (placeholder for future implementation)
        
        Args:
            audio_file: File-like object or path to audio file
            
        Returns:
            str: Message indicating the feature is not implemented
        """
        return "Chức năng xử lý âm thanh chưa được triển khai."