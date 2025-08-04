# LEGAL MIND
A Legal Query and Q&A Support Application 


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

Create a file named `.env` containing your API keys for Gemini (or TogetherAI if you prefer to use the LLama/DeepSeek model):  
```
TOGETHER_API_KEY= your_together_api_key
GEMINI_API_KEY= your_gemini_api_key
```

## How to Run the Application  
Install the required packages:  
```bash
pip install -r requirements.txt
```
Then launch the Streamlit app:
```bash
python -m streamlit run app.py
```

# Note on the Dataset
The dataset is reused from a competition and may not be fully accurate or up-to-date.
