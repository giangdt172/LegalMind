import os
import torch
import streamlit as st
from FlagEmbedding import BGEM3FlagModel
from src.config import Config

class EmbeddingModel:
    def __init__(self):
        self.config = Config()
        try:
            self.model = self.load_model()
        except Exception as e:
            st.error(f"Error loading embedding model: {str(e)}")
            self.model = None
        
    @st.cache_resource
    def load_model(_self):
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            if device == "cuda":
                os.environ["CUDA_VISIBLE_DEVICES"] = "0"
            
            model = BGEM3FlagModel(
                _self.config.EMBEDDING_MODEL, 
                use_fp16=True
            )
            return model
        except Exception as e:
            st.error(f"Failed to load embedding model: {str(e)}")
            return None
    
    @st.cache_data
    def get_query_embedding(_self, query):
        if _self.model is None:
            st.error("Embedding model is not loaded. Please check the model configuration.")
            return [0.0] * 768  # Assuming a standard embedding size
            
        try:
            embedding = _self.model.encode(
                [query],
                batch_size=32,
                max_length=512
            )['dense_vecs']
            
            return embedding[0]
        except Exception as e:
            st.error(f"Error generating embedding: {str(e)}")
            return [0.0] * 768  # Assuming a standard embedding size 