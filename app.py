import pandas as pd
import numpy as np
import torch
import os
import faiss
import streamlit as st
from FlagEmbedding import BGEM3FlagModel
from openai import OpenAI

st.set_page_config(
    page_title="LEGAL MIND",
    page_icon="⚖️",
    layout="wide"
)


st.markdown("""
<div style="background-color: #FF4B4B; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem;">
    <h1 style="color: white; margin: 0;">LEGAL MIND ⚖️</h1>
    <p style="color: white; margin-top: 0.5rem;">Hệ thống Tìm kiếm và Hỏi đáp Pháp luật</p>
</div>
""", unsafe_allow_html=True)


TOGETHER_API_KEY = 'API_KEY'

@st.cache_resource
def load_model():
    """Load the embedding model with caching to avoid reloading on each interaction"""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cuda":
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    
    model = BGEM3FlagModel('AITeamVN/Vietnamese_Embedding', use_fp16=True)
    return model

@st.cache_resource
def load_data():
    df = pd.read_csv('corpus.csv')
    df_embeddings = np.load("embedded_bge_train_law.npz")
    
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
    """Retrieve top-k documents based on FAISS similarity search"""
    model = load_model()
    
    query_embedding = get_query_embedding(query, model)
    
    if query_embedding.ndim == 1:
        query_embedding = query_embedding.reshape(1, -1)

    D, I = index.search(query_embedding, k)
    
    if len(I[0]) == 0:
        st.error("Không tìm thấy tài liệu nào phù hợp với truy vấn của bạn.")
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

def ask_llm(query, context=""):
    """Ask a question to the LLM using Together API"""
    try:
        client = OpenAI(api_key=TOGETHER_API_KEY, base_url="https://api.together.xyz/v1")
        
        # If we have context from retrieved documents, include it
        if context:
            system_prompt = (
                "Bạn là một người hiểu rất rõ về luật pháp của Việt Nam. "
                "Hãy dựa vào thông tin được cung cấp để trả lời câu hỏi. "
                "Nếu không có thông tin đủ để trả lời, hãy nói rõ điều đó."
            )
            user_prompt = f"Thông tin tham khảo:\n{context}\n\nCâu hỏi: {query}"
        else:
            system_prompt = "Bạn là một người hiểu rất rõ về luật pháp của Việt Nam"
            user_prompt = query
        
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Đã xảy ra lỗi khi gọi API: {str(e)}"

# Main application
def main():
    with st.spinner("Đang tải dữ liệu và mô hình..."):
        df, index = load_data()
    
    st.sidebar.title("Tùy chọn")
    
    app_mode = st.sidebar.radio(
        "Chọn chế độ:",
        ["Tìm kiếm tài liệu", "Hỏi đáp luật pháp", "Tìm kiếm + Hỏi đáp"]
    )
    
    if app_mode == "Tìm kiếm tài liệu":
        search_documents_ui(df, index)
    elif app_mode == "Hỏi đáp luật pháp":
        qa_ui()
    else:
        rag_ui(df, index)

    st.sidebar.markdown("---")
    st.sidebar.markdown("- Hỏi đáp: deepseek-ai/DeepSeek-V3")


def search_documents_ui(df, index):
    """UI for document search"""
    st.subheader("🔍 Tìm kiếm tài liệu")
    
    k = st.slider("Số lượng kết quả hiển thị", min_value=1, max_value=20, value=10)
    query = st.text_input("Nhập từ khóa tìm kiếm:")
    
    if st.button("Tìm kiếm", type="primary"):
        if query:
            with st.spinner("Đang tìm kiếm tài liệu liên quan..."):
                results = retrieve_documents(query, index, df, k=k)
            
            if results:
                st.success(f"Tìm thấy {len(results)} kết quả cho: '{query}'")
                
                for result in results:
                    with st.expander(f"📄 Tài liệu {result['rank']} (Điểm tương đồng: {1/(1+result['distance']):.4f})"):
                        st.markdown(result['text'])
            else:
                st.info("Không tìm thấy kết quả nào. Vui lòng thử lại với từ khóa khác.")
        else:
            st.warning("Vui lòng nhập từ khóa tìm kiếm.")

def qa_ui():
    st.subheader("❓ Hỏi đáp pháp luật")
    
    query = st.text_input("Nhập câu hỏi của bạn:")
    
    if st.button("Gửi câu hỏi", type="primary"):
        if query:
            with st.spinner("Đang xử lý câu hỏi của bạn..."):
                answer = ask_llm(query)
            
            st.subheader("Câu trả lời:")
            st.markdown(answer)
        else:
            st.warning("Vui lòng nhập câu hỏi.")

def rag_ui(df, index):
    st.subheader("🔍❓ Tìm kiếm và Hỏi đáp")
    
    query = st.text_input("Nhập câu hỏi của bạn:")
    k = st.slider("Số lượng tài liệu tham khảo", min_value=1, max_value=10, value=3)
    
    if st.button("Gửi câu hỏi", type="primary"):
        if query:
            with st.spinner("Đang tìm kiếm tài liệu liên quan..."):
                results = retrieve_documents(query, index, df, k=k)
            
            if results:
                context = "\n\n".join([f"Tài liệu {result['rank']}: {result['text']}" for result in results])
                
                with st.spinner("Đang xử lý câu trả lời..."):
                    answer = ask_llm(query, context)
                
                st.subheader("Câu trả lời:")
                st.markdown(answer)
                
                with st.expander("Xem tài liệu tham khảo"):
                    for result in results:
                        st.markdown(f"**Tài liệu {result['rank']}** (Điểm tương đồng: {1/(1+result['distance']):.4f})")
                        st.markdown(result['text'])
                        st.markdown("---")
            else:
                with st.spinner("Không tìm thấy tài liệu liên quan. Đang xử lý câu hỏi trực tiếp..."):
                    answer = ask_llm(query)
                
                st.subheader("Câu trả lời:")
                st.markdown(answer)
                st.info("Không tìm thấy tài liệu liên quan. Câu trả lời dựa trên kiến thức chung của mô hình.")
        else:
            st.warning("Vui lòng nhập câu hỏi.")

if __name__ == "__main__":
    main()
