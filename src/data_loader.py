import pandas as pd
import numpy as np
import faiss
import streamlit as st
import os
from src.config import Config

class DataLoader:
    def __init__(self):
        self.config = Config()
        self.df = None
        self.index = None
        self.cid_map = None
        
    @st.cache_resource
    def load_data(_self):
        _self.df = pd.read_csv(_self.config.CORPUS_PATH)
        
        df_embeddings = np.load(_self.config.EMBEDDINGS_PATH)
        
        embeddings_array = df_embeddings['embeddings'].astype('float32')
        _self.cid_map = df_embeddings['cid'].tolist()
        
        embeddings_array = np.ascontiguousarray(embeddings_array)

        dimension = embeddings_array.shape[1]
        _self.index = faiss.IndexFlatL2(dimension)
        _self.index.add(embeddings_array)
        
        return _self.df, _self.index
        
    def get_data(self):
        if self.df is None or self.index is None:
            self.df, self.index = self.load_data()
        return self.df, self.index 