import streamlit as st
from src.config import Config
from src.model import EmbeddingModel
from src.data import DataLoader
from src.retriever import Retriever
from src.llm import LLMClient
from ui.search_ui import SearchUI
from ui.rag_ui import RagUI
import logging
from typing import Tuple, Any

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def initialize_components() -> Tuple[Config, DataLoader, Retriever, LLMClient]:
    """Initialize all required components"""
    try:
        config = Config.from_env()
        data_loader = DataLoader(config.CORPUS_CSV, config.VECTORDB)
        embedding_model = EmbeddingModel(config.EMBEDDING_MODEL)
        retriever = Retriever(embedding_model, data_loader.get_index(), data_loader.get_data())
        llm_client = LLMClient(config)
        return config, data_loader, retriever, llm_client
    except Exception as e:
        logging.error(f"Error initializing components: {str(e)}")
        raise

def setup_page():
    """Setup Streamlit page configuration"""
    st.set_page_config(
        page_title="Legal Mind",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def main():
    """Main application entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        setup_page()
        config, data_loader, retriever, llm_client = initialize_components()
        
        # Sidebar
        st.sidebar.title("⚖️ LEGAL MIND")
        st.sidebar.markdown("---")
        app_mode = st.sidebar.radio(
            "Chọn chế độ:",
            ["Tìm kiếm tài liệu", "Tìm kiếm + Hỏi đáp"]
        )
        
        # Main content
        if app_mode == "Tìm kiếm tài liệu":
            SearchUI(retriever).render()
        else:
            RagUI(retriever, llm_client).render()
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("Đã có lỗi xảy ra. Vui lòng thử lại sau.")

if __name__ == "__main__":
    main()
