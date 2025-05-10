class CSSStyles:
    @staticmethod
    def get_styles():
        return """
<style>
    /* Biến màu sắc chính */
    :root {
        --primary-color: #4b6584;
        --primary-light: #7d95b6;
        --background-light: #f8f9fa;
        --text-dark: #2c3e50;
        --shadow: rgba(0,0,0,0.08);
    }
    
    /* Căn chỉnh chiều dọc cho các cột */
    .row-widget.stHorizontal {
        align-items: center !important;
        display: flex !important;
        gap: 10px !important; /* Khoảng cách giữa input và button */
    }
    
    /* Đảm bảo các container có cùng padding */
    .search-container {
        background-color: var(--background-light);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 12px var(--shadow);
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
    }
    
    /* Phong cách cho thanh tìm kiếm */
    .stTextInput > div {
        display: flex !important;
        align-items: center !important;
    }
    
    
    /* Phong cách cho nút */
    .stButton > button {
        border-radius: 30px !important;
        font-weight: 500 !important;
        padding: 0 25px !important;
        transition: all 0.3s ease !important;
        background-color: var(--primary-color) !important;
        color: white !important;
        height: 42px !important;
        margin: 0 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    
    /* Đảm bảo columns nằm trên cùng một dòng */
    div.row-widget.stHorizontal > div {
        align-items: center !important;
        padding-bottom: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Header chính */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.2rem;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
        font-size: 1rem;
    }
    
    /* Kết quả tìm kiếm */
    .result-item {
        border-left: 4px solid var(--primary-color);
        padding-left: 15px;
        margin-bottom: 15px;
    }
    
    /* Điều chỉnh kích thước tùy vào màn hình */
    @media (max-width: 768px) {
        .stTextInput input, .stButton > button {
            height: 38px !important;
        }
    }
</style>
""" 