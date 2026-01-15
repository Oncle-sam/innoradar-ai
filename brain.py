import google.generativeai as genai
import streamlit as st

def get_model():
    api_key = st.secrets.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # On utilise le nom EXACT que nous avons vu dans votre liste
    # Ce modèle est idéal car il est stable et performant en 2026
    model_name = 'models/gemini-2.0-flash' 
    
    model = genai.GenerativeModel(model_name=model_name)
    return model, model_name

def generate_response(model, prompt, history):
    # On inclut le Framework InnoRadar directement ici
    system_instructions = """
    Tu es l'intelligence centrale d'InnoRadar, expert en Sport Tech.
    Ton rôle est de diagnostiquer les besoins B2B et de proposer des solutions précises.
    MÉTHODE : Pose 5 questions clés avant de conclure.
    SCORE : Affiche toujours un 'Relevance Score' en % pour tes suggestions.
    """
    
    # Construction du contexte
    full_prompt = f"{system_instructions}\n\n"
    for msg in history:
        full_prompt += f"{msg['role']}: {msg['content']}\n"
    
    full_prompt += f"user: {prompt}"
    
    # Appel de génération
    response = model.generate_content(full_prompt)
    return response.text
