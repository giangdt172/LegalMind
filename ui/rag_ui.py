import streamlit as st
from typing import Optional, Tuple
from PIL import Image
from .base_ui import BaseUI

class RagUI(BaseUI):
    def __init__(self, retriever, llm_client):
        super().__init__()
        self.retriever = retriever
        self.llm_client = llm_client

    def handle_text_input(self) -> Tuple[Optional[str], bool]:
        """Handle text input mode"""
        query, ask_button = self.create_search_input("Nhập câu hỏi pháp lý của bạn...")
        if query:
            st.session_state.query_ready = True
            st.session_state.query_text = query
            st.session_state.query_source = "text"
        return query, ask_button

    def handle_image_input(self) -> Tuple[Optional[str], bool]:
        """Handle image input mode"""
        st.markdown("<p style='margin-bottom: 10px;'>Tải lên hình ảnh tài liệu để phân tích</p>", unsafe_allow_html=True)
        uploaded_image = st.file_uploader(
            "Chọn hình ảnh để đặt câu hỏi",
            type=["jpg", "jpeg", "png"],
            key="rag_image"
        )

        if not uploaded_image:
            return None, False

        col1, col2 = st.columns([3, 2])
        with col1:
            image = Image.open(uploaded_image)
            st.image(image, caption="Hình ảnh đã tải lên", use_container_width=True)
        
        with col2:
            st.markdown("<div style='padding:20px; background:#f8f9fa; border-radius:8px;'>", unsafe_allow_html=True)
            st.markdown("<h4>Phân tích hình ảnh</h4>", unsafe_allow_html=True)
            
            if st.button("🔍 Phân tích hình ảnh", key="process_rag_image", use_container_width=True):
                with st.spinner("Đang phân tích hình ảnh..."):
                    processed = self.llm_client.process_image(uploaded_image)
                st.success("Đã phân tích xong hình ảnh")
                st.markdown(f"<div style='padding:10px; background:white;'><strong>Nội dung trích xuất:</strong><br>{processed}</div>", unsafe_allow_html=True)
                st.session_state.query_ready = True
                st.session_state.query_text = processed
                st.session_state.query_source = "image"
                return processed, True
            
            ask_button = st.button("🔍 Tra cứu kết quả", key="rag_image_ask_btn", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        return None, ask_button

    def handle_audio_input(self) -> Tuple[Optional[str], bool]:
        """Handle audio input mode"""
        st.markdown("<p style='margin-bottom:10px;'>Tải lên file âm thanh để phân tích</p>", unsafe_allow_html=True)
        uploaded_audio = st.file_uploader(
            "Chọn file âm thanh để đặt câu hỏi",
            type=["mp3", "wav", "ogg"],
            key="rag_audio"
        )

        if not uploaded_audio:
            return None, False

        st.audio(uploaded_audio)
        if st.button("🎙️ Phân tích âm thanh", key="process_rag_audio", use_container_width=True):
            with st.spinner("Đang xử lý âm thanh..."):
                processed = self.llm_client.process_audio(uploaded_audio)
            st.success("Đã phân tích xong âm thanh")
            st.markdown(f"<div style='padding:10px; background:white;'><strong>Nội dung trích xuất:</strong><br>{processed}</div>", unsafe_allow_html=True)
            st.session_state.query_ready = True
            st.session_state.query_text = processed
            st.session_state.query_source = "audio"
            return processed, True

        ask_button = st.button("🤖 Tra cứu kết quả", key="rag_audio_ask_btn", use_container_width=True)
        return None, ask_button

    def process_query(self, query: str, query_type: str, k: int):
        """Process the query and display results"""
        with st.spinner("Đang tìm kiếm tài liệu liên quan..."):
            results = self.retriever.retrieve(query, k=k)

        if results:
            context = "\n\n".join([f"Tài liệu {r['rank']}: {r['text']}" for r in results])
            with st.spinner("Đang xử lý câu trả lời..."):
                if query_type in ("image", "audio"):
                    prompt = f"Dựa trên nội dung {query_type} được tóm tắt như sau: {query}, vui lòng cung cấp phân tích pháp lý liên quan"
                    answer = self.llm_client.ask(prompt, context)
                else:
                    answer = self.llm_client.ask(query, context)

            st.markdown("<h3 style='color: #4b6584; border-bottom:2px solid #4b6584; padding-bottom:10px;'>Câu trả lời:</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='background:white; padding:20px; border-radius:8px; border-left:5px solid #4b6584;'>{answer}</div>", unsafe_allow_html=True)
            
            with st.expander("Xem tài liệu tham khảo"):
                for idx, r in enumerate(results):
                    score = 1/(1+r['distance'])
                    st.markdown(f"**Tài liệu {idx+1}** (Score: {score:.4f})")
                    st.markdown(r['text'])
        else:
            self.show_info("Không tìm thấy tài liệu liên quan. Câu trả lời dựa trên kiến thức mô hình.")
            answer = self.llm_client.ask(query)
            st.markdown(f"<div style='background:white; padding:20px; border-radius:8px; border-left:5px solid #4b6584;'>{answer}</div>", unsafe_allow_html=True)

    def render(self):
        try:
            st.markdown("<h2 style='color: #4b6584;'>🔍 Tìm kiếm và Hỏi đáp thông minh</h2>", unsafe_allow_html=True)
            
            # Input method selection
            search_method = st.radio(
                "Chọn phương thức tìm kiếm:",
                ["Văn bản", "Hình ảnh", "Âm thanh"],
                horizontal=True,
                label_visibility="hidden"
            )

            # Handle different input methods
            if search_method == "Văn bản":
                query, ask_button = self.handle_text_input()
            elif search_method == "Hình ảnh":
                query, ask_button = self.handle_image_input()
            else:  # Audio
                query, ask_button = self.handle_audio_input()

            # Advanced options
            with st.expander("Tùy chọn nâng cao"):
                k = self.create_results_slider(min_value=1, max_value=10, default=3)

            # Process query if ready
            if ask_button or st.session_state.get("query_ready", False):
                final_query = st.session_state.get("query_text", "")
                query_type = st.session_state.get("query_source", "text")
                self.process_query(final_query, query_type, k)
                st.session_state.query_ready = False
            elif not query:
                self.show_warning("Vui lòng nhập câu hỏi hoặc tải lên media để đặt câu hỏi.")

        except Exception as e:
            self.show_error(f"Lỗi khi xử lý yêu cầu: {str(e)}")
