import streamlit as st
from typing import Optional, List, Dict, Any
import logging

class BaseUI:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def show_error(self, message: str):
        """Display error message to user"""
        self.logger.error(message)
        st.error(message)

    def show_success(self, message: str):
        """Display success message to user"""
        st.success(message)

    def show_info(self, message: str):
        """Display info message to user"""
        st.info(message)

    def show_warning(self, message: str):
        """Display warning message to user"""
        st.warning(message)

    def create_search_input(self, placeholder: str = "Nhập từ khóa tìm kiếm...") -> tuple[Optional[str], bool]:
        """Create a search input with button"""
        col1, col2 = st.columns([5, 1])
        with col1:
            query = st.text_input(
                "Từ khóa tìm kiếm",
                placeholder=placeholder,
                label_visibility="hidden"
            )
        with col2:
            search_button = st.button(
                "Tra cứu",
                type="primary",
                use_container_width=True
            )
        return query, search_button

    def create_results_slider(self, min_value: int = 1, max_value: int = 20, default: int = 10) -> int:
        """Create a slider for number of results"""
        return st.slider(
            "Số lượng kết quả hiển thị",
            min_value=min_value,
            max_value=max_value,
            value=default
        )

    def display_results(self, query: str, results: List[Dict[str, Any]]):
        """Display search results"""
        if not results:
            self.show_info("Không tìm thấy kết quả nào.")
            return

        self.show_success(f"Tìm thấy {len(results)} kết quả cho: '{query}'")
        for idx, result in enumerate(results, 1):
            with st.expander(f"Tài liệu {idx}"):
                st.markdown(result['text'])
                if 'score' in result:
                    st.caption(f"Độ phù hợp: {result['score']:.2f}") 