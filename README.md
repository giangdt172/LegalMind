# LEGAL MIND
Ứng dụng Hỗ trợ truy vẫn và hỏi đáp về pháp luật


## Project Structure
```
|── app.py                          # Main application
├── data/              
│   ├── corpus.csv                  # legal corpus data
│   └── embedded_bge_train_law.npz  # embedded data
├── src/                   
│   ├── config          
│   ├── data_loader
│   │── model_loader             
│   ├── retriever      
│   └── llm_service        
│              
└── ui/                    
    ├── search_documents.py  
    ├── rag_ui.py          
    ├── app_ui.py         
    └── css_styles.py      
```

## Environment Variables

Cần tạo file `.env` chứa API của Gemini (hoặc TogetherAI nếu muốn sử dụng model LLama/DeepSeek):

```
TOGETHER_API_KEY= your_together_api_key
GEMINI_API_KEY= your_gemini_api_key
```

## Hướng dẫn chạy ứng dụng
Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```
Trong terminal chạy lệnh sau:
```bash
python -m streamlit run app.py
```

## Dataset được sử dụng lại từ cuộc thi nên có thể không chính xác và cập nhật mới nhất