from dataclasses import dataclass
import os
from dotenv import load_dotenv

@dataclass
class Config:
    GEMINI_API_KEY: str
    EMBEDDING_MODEL: str = "AITeamVN/Vietnamese_Embedding"
    CORPUS_CSV: str = "data/corpus.csv"
    VECTORDB: str = "data/vectordb"
    MAX_RESULTS: int = 10
    DEFAULT_K: int = 3
    
    @classmethod
    def from_env(cls) -> 'Config':
        load_dotenv()
        return cls(
            GEMINI_API_KEY=os.getenv("GEMINI_API_KEY", ""),
            EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL", cls.EMBEDDING_MODEL),
            CORPUS_CSV=os.getenv("CORPUS_CSV", cls.CORPUS_CSV),
            VECTORDB=os.getenv("VECTORDB", cls.VECTORDB),
            MAX_RESULTS=int(os.getenv("MAX_RESULTS", cls.MAX_RESULTS)),
            DEFAULT_K=int(os.getenv("DEFAULT_K", cls.DEFAULT_K))
        )
