import numpy as np
import streamlit as st
from src.model_loader import EmbeddingModel

class Retriever:
    def __init__(self, embedding_model=None):
        if embedding_model is None:
            self.embedding_model = EmbeddingModel()
        else:
            self.embedding_model = embedding_model
    
    @st.cache_data(show_spinner=False)
    def get_query_embedding(_self, query):
        return _self.embedding_model.get_query_embedding(query)
    
    def retrieve_documents(self, query, index, df, k=10):
        try:
            query_embedding = self.get_query_embedding(query)
            query_embedding = np.array(query_embedding, dtype=np.float32)
          
            if query_embedding.ndim == 1:
                query_embedding = query_embedding.reshape(1, -1)

            D, I = index.search(query_embedding, k)
            
            if len(I[0]) == 0:
                return []

            documents = df["text"].tolist()
            results = []
            
            for idx, doc_idx in enumerate(I[0]):
                results.append({
                    "rank": idx + 1,
                    "distance": D[0][idx],
                    "text": documents[doc_idx]
                })
            
            return results
        except Exception as e:
            st.error(f"Error retrieving documents: {str(e)}")
            return [] 