import google.generativeai as genai
import streamlit as st

# Diagnostic : Liste des modèles
st.sidebar.title("🔍 Diagnostic API")

try:
    api_key = st.secrets.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # Appel à ListModels
    models = genai.list_models()
    
    st.sidebar.write("Modèles autorisés pour votre clé :")
    for m in models:
        # On affiche le nom et les méthodes supportées (ex: generateContent)
        if 'generateContent' in m.supported_generation_methods:
            st.sidebar.code(m.name) # Affiche le nom exact à copier
            
except Exception as e:
    st.sidebar.error(f"Erreur ListModels : {e}")
