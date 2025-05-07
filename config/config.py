from dotenv import load_dotenv
import os
load_dotenv()

class ConfigLLM:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")