import torch
import os
from FlagEmbedding import BGEM3FlagModel

class EmbeddingModel:
    def __init__(self, model_name):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device == "cuda":
            os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        self.model = BGEM3FlagModel(model_name, use_fp16=True)

    def get_query_embedding(self, query):
        embedding = self.model.encode([query], batch_size=32, max_length=512)['dense_vecs'][0]
        return embedding