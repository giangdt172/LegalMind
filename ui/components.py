import streamlit as st
from typing import Optional, Callable
from PIL import Image

class InputHandler:
    @staticmethod
    def text_input() -> tuple[Optional[str], bool]:
        col1, col2 = st.columns([5, 1])
        with col1:
            query = st.text_input(
                "Câu hỏi pháp lý",
                placeholder="Nhập câu hỏi pháp lý của bạn...",
                key="rag_text_query",
                label_visibility="hidden"
            )
        with col2:
            ask_button = st.button(
                "🔍 Tra cứu",
                type="primary",
                use_container_width=True,
                key="rag_ask_btn"
            )
        return query, ask_button

    @staticmethod
    def image_input(process_callback: Callable) -> tuple[Optional[str], bool]:
        uploaded_image = st.file_uploader(
            "Chọn hình ảnh để đặt câu hỏi",
            type=["jpg", "jpeg", "png"],
            key="rag_image"
        )
        
        if uploaded_image:
            col1, col2 = st.columns([3, 2])
            with col1:
                image = Image.open(uploaded_image)
                st.image(image, caption="Hình ảnh đã tải lên", use_container_width=True)
            with col2:
                st.markdown("<div style='padding:20px; background:#f8f9fa; border-radius:8px;'>", unsafe_allow_html=True)
                st.markdown("<h4>Phân tích hình ảnh</h4>", unsafe_allow_html=True)
                
                if st.button("�� Phân tích hình ảnh", key="process_rag_image", use_container_width=True):
                    with st.spinner("Đang phân tích hình ảnh..."):
                        processed = process_callback(uploaded_image)
                    st.success("Đã phân tích xong hình ảnh")
                    st.markdown(f"<div style='padding:10px; background:white;'><strong>Nội dung trích xuất:</strong><br>{processed}</div>", unsafe_allow_html=True)
                    return processed, True
                
                ask_button = st.button("🔍 Tra cứu kết quả", key="rag_image_ask_btn", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        return None, False

class ResultDisplay:
    @staticmethod
    def show_results(query: str, results: list, answer: str):
        st.markdown("<div style='background:#f8f9fa; padding:20px; border-radius:10px; margin-top:20px; border:1px solid #e9ecef;'>", unsafe_allow_html=True)
        
        if results:
            st.success(f"Tìm thấy {len(results)} kết quả cho: '{query}'")
            st.markdown("<h3 style='color: #4b6584; border-bottom:2px solid #4b6584; padding-bottom:10px;'>Câu trả lời:</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='background:white; padding:20px; border-radius:8px; border-left:5px solid #4b6584;'>{answer}</div>", unsafe_allow_html=True)
            
            with st.expander("Xem tài liệu tham khảo"):
                for idx, r in enumerate(results):
                    score = 1/(1+r['distance'])
                    st.markdown(f"**Tài liệu {idx+1}** (Score: {score:.4f})")
                    st.markdown(r['text'])
        else:
            st.info("Không tìm thấy tài liệu liên quan. Câu trả lời dựa trên kiến thức mô hình.")
            st.markdown(f"<div style='background:white; padding:20px; border-radius:8px; border-left:5px solid #4b6584;'>{answer}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True) 