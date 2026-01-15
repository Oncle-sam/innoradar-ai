import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        .main { background-color: #000000; }
        .stButton>button {
            background: linear-gradient(45deg, #1B1464, #4433FF);
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px 24px;
        }
        div[data-testid="stSidebar"] {
            background-color: #0D0D1A;
            border-right: 1px solid #1B1464;
        }
        /* Style pour les messages de l'IA */
        .stChatMessage {
            border-radius: 15px;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True)