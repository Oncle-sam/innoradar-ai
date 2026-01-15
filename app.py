import streamlit as st
from styles import apply_styles
from brain import get_model, generate_response

# Configuration
st.set_page_config(page_title="Innoradar", page_icon="🚀", layout="wide")
apply_styles()

st.title("InnoRadar")
st.write("L'outil IA de matchmaking parfait connectant les acteurs du sport aux innovations vraiment utiles.")

# Initialisation du modèle
try:
    model = get_model()
except Exception as e:
    st.error(f"Erreur de connexion à l'IA : {e}")
    st.stop()

# Gestion du Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Posez votre question à InnoRadar..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = generate_response(model, prompt, st.session_state.messages)
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
