import google.generativeai as genai
import streamlit as st

# Votre Framework InnoRadar
SYSTEM_PROMPT = """
Tu es l'intelligence centrale d'InnoRadar, plateforme de matchmaking B2B Sport Tech.
Identité : Expert consultant Sport Tech de classe mondiale.
MÉTHODOLOGIE : 
1. Pose obligatoirement 5 questions pour cadrer le projet (Objectifs, Parties prenantes, Contraintes, Timeline, Budget).
2. Pour chaque solution proposée, affiche : Relevance Score (%), Impact Clé, Audit de Confiance (X/100), Faisabilité.
TON : Institutionnel, visionnaire, bilingue.
"""

def get_model():
    api_key = st.secrets.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # On essaie le nom le plus simple (souvent mappé sur la version stable v1)
    # Si 'gemini-pro' échoue, essayez 'gemini-1.5-flash'
    model_name = 'gemini-pro' 
    
    try:
        model = genai.GenerativeModel(model_name=model_name)
        # On ne fait pas de test de génération ici pour éviter le crash immédiat
        return model, model_name
    except Exception as e:
        raise Exception(f"Erreur lors de l'initialisation : {e}")


def generate_response(model, prompt, history):
    # On construit le prompt en mettant le framework AU DÉBUT
    # C'est ce qu'on appelle le "Prompt Injection" volontaire pour guider l'IA
    full_prompt = f"INSTRUCTIONS SYSTÈME:\n{SYSTEM_PROMPT}\n\n"
    
    # On ajoute l'historique
    for msg in history:
        role = "Utilisateur" if msg["role"] == "user" else "Assistant"
        full_prompt += f"{role}: {msg['content']}\n"
    
    # On ajoute la nouvelle question
    full_prompt += f"\nUtilisateur: {prompt}\nAssistant:"
    
    # Appel simplifié
    response = model.generate_content(
        full_prompt,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 2000,
        }
    )
    return response.text
