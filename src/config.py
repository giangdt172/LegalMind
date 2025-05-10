import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()

        self.TOGETHER_API_KEY = os.environ.get('TOGETHER_API_KEY')
        self.GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

        self.CORPUS_PATH = os.path.join('data', 'corpus.csv')
        self.EMBEDDINGS_PATH = os.path.join('data', 'embedded_bge_train_law.npz')

        self.APP_TITLE = "LEGAL MIND"
        self.APP_ICON = "⚖️"
        self.APP_LAYOUT = "wide"

        self.EMBEDDING_MODEL = 'AITeamVN/Vietnamese_Embedding'
        self.LLM_MODEL = 'gemini-2.0-flash' 