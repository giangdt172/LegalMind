import streamlit as st
from ui.css_styles import CSSStyles
from ui.search_documents import SearchDocumentsUI
from ui.rag_ui import RAGUI
from src.config import Config

class AppUI:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.config = Config()
        self.search_ui = SearchDocumentsUI(data_loader)
        self.rag_ui = RAGUI(data_loader)
    
    def apply_css_styles(self):
        st.markdown(CSSStyles.get_styles(), unsafe_allow_html=True)
    
    def render_header(self):
        st.markdown("""
        <div class="main-header">
            <h1>LEGAL MIND ⚖️</h1>
            <p>Trợ lý Pháp lý AI</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        st.sidebar.markdown("""
        <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, #4b6584 0%, #7d95b6 100%); border-radius: 10px; margin-bottom: 20px;">
            <h2 style="color: white; margin: 0; font-size: 1.5rem;">⚖️ LEGAL MIND</h2>
        </div>
        """, unsafe_allow_html=True)

        st.sidebar.markdown("<h3 style='margin-top:0;'>Tùy chọn</h3>", unsafe_allow_html=True)
        
        app_mode = st.sidebar.radio(
            "Chọn chế độ:",
            ["Tìm kiếm tài liệu", "Tìm kiếm + Hỏi đáp"],
            format_func=lambda x: f"📚 {x}" if x == "Tìm kiếm tài liệu" else f"🤖 {x}"
        )
        
        st.sidebar.markdown("---")
        
        with st.sidebar.expander("ℹ️ Giới thiệu"):
            st.markdown("""
            **LEGAL MIND** là hệ thống tìm kiếm và hỏi đáp thông minh về pháp luật Việt Nam.
            
            Hệ thống sử dụng công nghệ AI tiên tiến để giúp bạn tìm kiếm và hiểu rõ các vấn đề pháp lý.
            """)
        
        with st.sidebar.expander("📝 Hướng dẫn sử dụng"):
            st.markdown("""
            - **Tìm kiếm tài liệu**: Nhập từ khóa để tìm kiếm tài liệu pháp luật liên quan
            - **Tìm kiếm + Hỏi đáp**: Đặt câu hỏi và nhận câu trả lời dựa trên tài liệu pháp luật
            - Sử dụng các phương tiện như hình ảnh hoặc âm thanh để đặt câu hỏi
            """)
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("<div style='text-align:center; opacity:0.7;'>© 2025 LEGAL MIND</div>", unsafe_allow_html=True)
        
        return app_mode
    
    def render(self):
        self.apply_css_styles()
        self.render_header()
        app_mode = self.render_sidebar()
        
        if app_mode == "Tìm kiếm tài liệu":
            self.search_ui.render()
        else:
            self.rag_ui.render() 
