import streamlit as st
import google.generativeai as genai


# --- INTERFACE UTILISATEUR ---
st.set_page_config(page_title="Innoradar", page_icon="🚀", layout="wide")

st.title("InnoRadar")
st.write("L'outil IA de matchmaking parfait connectant les acteurs du sport aux innovations vraiment utiles.")


# CSS pour l'esthétique Glassmorphism et typographie
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
    </style>
    """, unsafe_allow_html=True)


# 2. Sécurité & Modèle

# Configuration selon AI Studio
generation_config = {
  "temperature": 0.5,
  "top_p": 0.9,
  "top_k": 40,
  "max_output_tokens": 4000,
}


api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Clé API manquante. Configurez GEMINI_API_KEY dans les secrets.")
    st.stop()

# 1. Configuration de l'API (forcez la configuration globale)
genai.configure(api_key=api_key)

# 2. Testez ce nom de modèle précis (sans le préfixe models/ cette fois, 
# car la bibliothèque l'ajoute parfois d'elle-même selon la version)
MODEL_NAME = 'gemini-1.5-flash-latest' 

# 3. Framework InnoRadar (System Instruction)
SYSTEM_PROMPT = """
Tu es l'intelligence centrale d'InnoRadar, plateforme de matchmaking B2B Sport Tech.
TON : Institutionnel, visionnaire, bilingue.
MÉTHODOLOGIE : 
1. Pose obligatoirement 5 questions pour cadrer le projet (Objectifs, Parties prenantes, Contraintes, Timeline, Budget).
2. Pour chaque solution proposée, affiche :
   - Relevance Score (%)
   - Impact Clé (KPI chiffré)
   - Audit de Confiance (X/100)
   - Faisabilité (Mode éco + temps d'implémentation)
3. Produit Signature : Si besoin complexe, propose "InnoRadar AI Factory".
"""

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=generation_config,
    system_instruction=SYSTEM_PROMPT
)

# 4. Interface Chat

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utilisateur
if prompt := st.chat_input("Décrivez votre besoin ou votre challenge sportif..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# 5. Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/1B1464/FFFFFF?text=INNORADAR", use_container_width=True)
    st.write("---")
    st.info("Expertise : Consultant Sport Tech\nMode : Diagnostic & Matchmaking")
    if st.button("Nouvelle Analyse"):
        st.session_state.messages = []
        st.rerun()
