import streamlit as st
from src.retriever import Retriever

class SearchDocumentsUI:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.retriever = Retriever()
    
    def render(self):
        """Render the document search UI"""
        df, index = self.data_loader.get_data()
        
        st.markdown("<h2 style='color: #4b6584;'>🔍 Tìm kiếm tài liệu pháp luật</h2>", unsafe_allow_html=True)
        
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([5, 1])
        
        with col1:
            query = st.text_input(
                    "Từ khóa tìm kiếm", 
                    placeholder="Nhập từ khóa tìm kiếm...", 
                    label_visibility="hidden",
                    help="Nhập các từ khóa liên quan đến nội dung pháp luật bạn cần tìm")
        
        with col2:
            search_button = st.button("🔍 Tra cứu", type="primary", use_container_width=True, key="rag_ask_btn")
        
        with st.expander("Tuỳ chọn tìm kiếm nâng cao"):
            k = st.slider("Số lượng kết quả hiển thị", min_value=1, max_value=20, value=10)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        self._handle_search(query, search_button, index, df, k)
    
    def _handle_search(self, query, search_button, index, df, k):
        """Handle search logic and display results"""
        if search_button or query:
            if query:
                with st.spinner("Đang tìm kiếm tài liệu liên quan..."):
                    results = self.retriever.retrieve_documents(query, index, df, k=k)
                
                if results:
                    st.success(f"Tìm thấy {len(results)} kết quả cho: '{query}'")
                    
                    st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
                    
                    for idx, result in enumerate(results):
                        relevance_score = 1/(1+result['distance'])
                        
                        background_color = f"rgba(75, 101, 132, {min(relevance_score, 0.3)})"
                        
                        st.markdown(f"""
                        <div style="padding: 15px; border-radius: 8px; margin-bottom: 15px; background-color: {background_color}; border-left: 5px solid #4b6584;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <h3 style="margin: 0; color: #2c3e50;">Tài liệu {idx + 1}</h3>
                                <span style="background-color: #4b6584; color: white; padding: 3px 10px; border-radius: 15px; font-size: 14px;">
                                    Độ phù hợp: {relevance_score}%
                                </span>
                            </div>
                            <div style="background-color: white; padding: 15px; border-radius: 5px; max-height: 200px; overflow-y: auto;">
                                {result['text']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("Không tìm thấy kết quả nào. Vui lòng thử lại với từ khóa khác.")
            else:
                st.warning("Vui lòng nhập từ khóa tìm kiếm.") 