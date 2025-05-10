import os
import shutil
import streamlit as st

# Set page config as first command
st.set_page_config(
    page_title="LEGAL MIND",
    page_icon="⚖️",
    layout="wide"
)

from src.data_loader import DataLoader
from ui.app_ui import AppUI

def setup_data():   
    if not os.path.exists(os.path.join('data', 'corpus.csv')) and os.path.exists('corpus.csv'):
        print("Moving corpus.csv to data directory...")
        shutil.copy('corpus.csv', os.path.join('data', 'corpus.csv'))

    if not os.path.exists(os.path.join('data', 'embedded_bge_train_law.npz')) and os.path.exists('embedded_bge_train_law.npz'):
        print("Moving embedded_bge_train_law.npz to data directory...")
        shutil.copy('embedded_bge_train_law.npz', os.path.join('data', 'embedded_bge_train_law.npz'))

def main():
    setup_data()
    data_loader = DataLoader()

    app = AppUI(data_loader)
    app.render()

if __name__ == "__main__":
    main() 