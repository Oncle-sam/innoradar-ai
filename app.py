import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE L'IA ---
# On récupère la clé de manière sécurisée (on verra cela à l'étape 5)
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Clé API manquante. Veuillez la configurer dans les secrets.")
    st.stop()

genai.configure(api_key=api_key)

# --- CONFIGURATION DE LA PERSONNALITÉ ---
SYSTEM_PROMPT = """
Tu es Innoradar AI, un expert en analyse d'innovation. 
Ton rôle est d'analyser les projets tech et sportifs selon les critères suivants :
1. Degré de rupture technologique.
2. Viabilité sur le marché.
3. Impact potentiel.
Réponds toujours de manière structurée et professionnelle.
"""

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=SYSTEM_PROMPT
)

# --- INTERFACE UTILISATEUR ---
st.set_page_config(page_title="Innoradar", page_icon="🚀")

st.title("🚀 Mon Application Gemini Bêta")
st.write("Bienvenue dans cette version test. Posez votre question ci-dessous.")

# Historique de chat (pour le côté interactif)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages précédents
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Dites quelque chose..."):
    # Afficher le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse de l'IA
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Appel à Gemini
            response = model.generate_content(prompt)
            full_response = response.text
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Erreur : {e}")
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})