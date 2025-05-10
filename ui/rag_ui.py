import streamlit as st
from PIL import Image
from src.retriever import Retriever
from src.llm_service import LLMService

class RAGUI:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.retriever = Retriever()
        self.llm_service = LLMService()
    
    def render(self):
        df, index = self.data_loader.get_data()
        
        st.markdown("<h2 style='color: #4b6584;'>🔍 Tìm kiếm và Hỏi đáp thông minh</h2>", unsafe_allow_html=True)
        
        ask_button = False
        
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        search_method = st.radio(
            "Chọn phương thức tìm kiếm:",
            ["Văn bản", "Hình ảnh", "Âm thanh"],
            horizontal=True,
            label_visibility="hidden" 
        )
        
        if 'query_ready' not in st.session_state:
            st.session_state.query_ready = False
        if 'query_text' not in st.session_state:
            st.session_state.query_text = ""
        if 'query_source' not in st.session_state:
            st.session_state.query_source = "text"
        
        if search_method == "Văn bản":
            self.text_search(ask_button)
        elif search_method == "Hình ảnh":
            self.image_search(ask_button)
        elif search_method == "Âm thanh":
            self.audio_search(ask_button)
        
        with st.expander("Tùy chọn nâng cao"):
            k = st.slider("Số lượng tài liệu tham khảo", min_value=1, max_value=10, value=3, key="rag_docs_count")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if ask_button or ('query_ready' in st.session_state and st.session_state.query_ready):
            self._process_query(df, index, k)
    
    def text_search(self, ask_button):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            query = st.text_input(
                "Câu hỏi pháp lý",
                placeholder="Nhập câu hỏi pháp lý của bạn...",
                key="rag_text_query",
                label_visibility="hidden",
                help="Nhập câu hỏi về vấn đề pháp lý bạn cần giải đáp"
            )
        
        with col2:
            ask_button = st.button("🔍 Tra cứu", type="primary", use_container_width=True, key="rag_ask_btn")
        
        if query:
            st.session_state.query_ready = True
            st.session_state.query_text = query
            st.session_state.query_source = "text"
    
    def image_search(self, ask_button):
        st.markdown("<p style='margin-bottom: 10px;'>Tải lên hình ảnh tài liệu để phân tích</p>", unsafe_allow_html=True)
        
        uploaded_image = st.file_uploader(
            "Chọn hình ảnh để đặt câu hỏi", 
            type=["jpg", "jpeg", "png"],
            key="rag_image",
            help="Tải lên hình ảnh chứa thông tin pháp lý"
        )
        
        if uploaded_image:
            col1, col2 = st.columns([3, 2])
            
            with col1:
                image = Image.open(uploaded_image)
                st.image(image, caption="Hình ảnh đã tải lên", use_container_width=True)
            
            with col2:
                st.markdown("<div style='padding: 20px; background-color: #f8f9fa; border-radius: 8px; height: 100%;'>", unsafe_allow_html=True)
                st.markdown("<h4>Phân tích hình ảnh</h4>", unsafe_allow_html=True)
                process_image_button = st.button("🔍 Phân tích hình ảnh", key="process_rag_image", use_container_width=True)
                
                if process_image_button:
                    with st.spinner("Đang phân tích hình ảnh..."):
                        processed_query = self.llm_service.process_image(uploaded_image)
                        st.session_state.image_rag_query = processed_query
                        st.session_state.query_source = "image"
                        
                    st.success("Đã phân tích xong hình ảnh")
                    st.markdown(f"<div style='padding: 10px; background-color: white; border-radius: 5px;'><strong>Nội dung trích xuất:</strong><br>{processed_query}</div>", unsafe_allow_html=True)
                    
                    st.session_state.query_ready = True
                    st.session_state.query_text = processed_query
                
                ask_button = st.button("🔍 Tra cứu kết quả", type="primary", use_container_width=True, key="rag_image_ask_btn")
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    def audio_search(self, ask_button):
        st.markdown("<p style='margin-bottom: 10px;'>Tải lên file âm thanh để phân tích</p>", unsafe_allow_html=True)
        
        uploaded_audio = st.file_uploader(
            "Chọn file âm thanh để đặt câu hỏi", 
            type=["mp3", "wav", "ogg"], 
            key="rag_audio",
            help="Tải lên file âm thanh chứa câu hỏi pháp lý"
        )
        
        if uploaded_audio:
            st.audio(uploaded_audio, format="audio/wav")
            
            process_audio_button = st.button("🎙️ Phân tích âm thanh", key="process_rag_audio", use_container_width=True)
            if process_audio_button:
                with st.spinner("Đang xử lý âm thanh..."):
                    processed_query = self.llm_service.process_audio(uploaded_audio)
                    st.session_state.audio_rag_query = processed_query
                    st.session_state.query_source = "audio"
                    
                st.success("Đã phân tích xong âm thanh")
                st.markdown(f"<div style='padding: 10px; background-color: white; border-radius: 5px; border-left: 4px solid #4b6584;'><strong>Nội dung trích xuất:</strong><br>{processed_query}</div>", unsafe_allow_html=True)
                
                st.session_state.query_ready = True
                st.session_state.query_text = processed_query
            
            ask_button = st.button("🤖 Tra cứu kết quả", type="primary", use_container_width=True, key="rag_audio_ask_btn")
    
    def _process_query(self, df, index, k):
        if 'query_text' in st.session_state and st.session_state.query_text:
            final_query = st.session_state.query_text
            query_type = st.session_state.query_source if 'query_source' in st.session_state else "text"
            
            st.markdown("<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px; border: 1px solid #e9ecef;'>", unsafe_allow_html=True)
            
            with st.spinner("Đang tìm kiếm tài liệu liên quan..."):
                results = self.retriever.retrieve_documents(final_query, index, df, k=k)
            
            if results:
                context = "\n\n".join([f"Tài liệu {result['rank']}: {result['text']}" for result in results])
                
                with st.spinner("Đang xử lý câu trả lời..."):
                    if query_type == "image":
                        answer = self.llm_service.ask_llm(
                            f"Dựa trên nội dung âm thanh được tóm tắt như sau: {final_query}, vui lòng cung cấp phân tích pháp lý liên quan. Không cung cấp thông tin không liên quan như lưu ý, disclaimer", 
                            context
                        )
                    elif query_type == "audio":
                        answer = self.llm_service.ask_llm(
                            f"Dựa trên nội dung âm thanh được tóm tắt như sau: {final_query}, vui lòng cung cấp phân tích pháp lý liên quan", 
                            context
                        )
                    else:
                        answer = self.llm_service.ask_llm(final_query, context)
                
                st.markdown("<h3 style='color: #4b6584; border-bottom: 2px solid #4b6584; padding-bottom: 10px;'>Câu trả lời:</h3>", unsafe_allow_html=True)
                
                st.markdown(f"<div style='background-color: white; padding: 20px; border-radius: 8px; border-left: 5px solid #4b6584;'>{answer}</div>", unsafe_allow_html=True)
                
                with st.expander("Xem tài liệu tham khảo"):
                    for idx, result in enumerate(results):
                        relevance_score = 1/(1+result['distance'])
                        st.markdown(f"<div class='result-item'><strong>Tài liệu {idx+1}</strong> (Độ tương đồng: {relevance_score:.4f})</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='padding: 10px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 15px;'>{result['text']}</div>", unsafe_allow_html=True)
            else:
                with st.spinner("Không tìm thấy tài liệu liên quan. Đang xử lý câu hỏi trực tiếp..."):
                    if query_type == "image":
                        answer = self.llm_service.ask_llm(f"Dựa trên hình ảnh được mô tả như sau: {final_query}, vui lòng cung cấp phân tích pháp lý liên quan")
                    elif query_type == "audio":
                        answer = self.llm_service.ask_llm(f"Dựa trên nội dung âm thanh được tóm tắt như sau: {final_query}, vui lòng cung cấp phân tích pháp lý liên quan")
                    else:
                        answer = self.llm_service.ask_llm(final_query)
                
                st.markdown("<h3 style='color: #4b6584; border-bottom: 2px solid #4b6584; padding-bottom: 10px;'>Câu trả lời:</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='background-color: white; padding: 20px; border-radius: 8px; border-left: 5px solid #4b6584;'>{answer}</div>", unsafe_allow_html=True)
                st.info("Không tìm thấy tài liệu liên quan. Câu trả lời dựa trên kiến thức chung của mô hình.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.session_state.query_ready = False
        else:
            st.warning("Vui lòng nhập câu hỏi hoặc tải lên media để đặt câu hỏi.") 