import pandas as pd
import numpy as np
import faiss

class DataLoader:
    def __init__(self, csv_path, npz_path):
        self.df = pd.read_csv(csv_path)
        df_embeddings = np.load(npz_path)
        self.embeddings_array = df_embeddings['embeddings'].astype('float32')
        self.embeddings_array = np.ascontiguousarray(self.embeddings_array)
        self.dimension = self.embeddings_array.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(self.embeddings_array)

    def get_data(self):
        return self.df

    def get_index(self):
        return self.index
