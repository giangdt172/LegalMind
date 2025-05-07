import pandas as pd
import numpy as np
import os
import torch
from FlagEmbedding import BGEM3FlagModel
import faiss

def load_model():
    """Load the embedding model with caching to avoid reloading on each interaction"""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cuda":
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    
    model = BGEM3FlagModel('AITeamVN/Vietnamese_Embedding', use_fp16=True)
    return model

def load_data():
    df = pd.read_csv('corpus.csv')
    df_embeddings = np.load("data/embedded_bge_train_law.npz")
    
    embeddings_array = df_embeddings['embeddings'].astype('float32')
    cid_map = df_embeddings['cid'].tolist()
    
    embeddings_array = np.ascontiguousarray(embeddings_array)

    dimension = embeddings_array.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings_array)
    
    return df, index

def get_query_embedding(query, model):
    embedding = model.encode(
        [query],
        batch_size=32,
        max_length=512
    )['dense_vecs']
    embedding = embedding[0]
    return np.array(embedding, dtype=np.float32)

def retrieve_documents(query, index, df, k=10):
    model = load_model()
    
    query_embedding = get_query_embedding(query, model)
    
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