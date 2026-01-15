import google.generativeai as genai
import streamlit as st

SYSTEM_PROMPT = """
Tu es l'intelligence centrale d'InnoRadar...
[Collez ici votre Framework complet]
"""

def get_model():
    api_key = st.secrets.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # On utilise le nom le plus stable
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        generation_config={
            "temperature": 0.5,
            "top_p": 0.9,
            "max_output_tokens": 4000,
        }
    )
    return model

def generate_response(model, prompt, history):
    # On fusionne les instructions et l'historique si besoin
    full_prompt = f"{SYSTEM_PROMPT}\n\nUtilisateur: {prompt}"
    response = model.generate_content(full_prompt)
    return response.text