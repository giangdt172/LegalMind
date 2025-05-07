import streamlit as st
from typing import Optional
from .base_ui import BaseUI

class SearchUI(BaseUI):
    def __init__(self, retriever):
        super().__init__()
        self.retriever = retriever

    def render(self):
        try:
            st.markdown("<h2 style='color: #4b6584;'>🔍 Tìm kiếm tài liệu pháp luật</h2>", unsafe_allow_html=True)
            
            query, search_button = self.create_search_input()
            
            k = self.create_results_slider()

            if search_button or query:
                if not query:
                    self.show_warning("Vui lòng nhập từ khóa tìm kiếm.")
                    return

                with st.spinner("Đang tìm kiếm..."):
                    results = self.retriever.retrieve(query, k=k)
                    self.display_results(query, results)

        except Exception as e:
            self.show_error(f"Lỗi khi tìm kiếm: {str(e)}")
