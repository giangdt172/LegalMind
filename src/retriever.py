class Retriever:
    def __init__(self, embedding_model, index, dataframe):
        self.embedding_model = embedding_model
        self.index = index
        self.df = dataframe

    def retrieve(self, query, k=10):
        query_embedding = self.embedding_model.get_query_embedding(query)
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        D, I = self.index.search(query_embedding, k)
        documents = self.df["text"].tolist()
        results = []
        for idx, doc_idx in enumerate(I[0]):
            results.append({
                "rank": idx + 1,
                "distance": D[0][idx],
                "text": documents[doc_idx]
            })
        return results
