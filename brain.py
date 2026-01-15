import google.generativeai as genai
import streamlit as st
import pandas as pd

def load_solutions():
    try:
        # Chargement du fichier
        df = pd.read_csv("solutions.csv")
        
        # Sélection stricte des colonnes publiques (Sécurité)
        cols_publiques = [
            "Dénomination actuelle", 
            "Type d'innovation", 
            "Type de produits / services", 
            "Sport ciblé", 
            "Résumé", 
            "Cas d'usage", 
            "Caractéristiques clés / proposition de valeur",
            "Site internet"
        ]
        
        # On ne garde que les colonnes qui existent vraiment dans le fichier
        available_cols = [c for c in cols_publiques if c in df.columns]
        df_public = df[available_cols].fillna("Non renseigné")
        
        return df_public
    except Exception as e:
        # En cas d'erreur de lecture, on renvoie un DataFrame vide
        return pd.DataFrame()

def get_model():
    api_key = st.secrets.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    # Utilisation du modèle confirmé lors de notre test ListModels
    model_name = 'models/gemini-2.0-flash'
    model = genai.GenerativeModel(model_name=model_name)
    return model, model_name


import google.generativeai as genai
import streamlit as st
import pandas as pd

# Le Framework définitif
QUESTIONS = [
    "quels sont les objectifs prioritaires de votre projet ?",
    "quelles sont les parties prenantes clés impliquées (Marketing, IT, Staff...) ?",
    "quels sont les impératifs techniques (CRM, Mobile-First, Wi-Fi...) ?",
    "quel est votre horizon de déploiement (Prochaine saison, 6 mois...) ?",
    "quelle est l'enveloppe budgétaire estimée ?"
]

def generate_response(model, prompt, history):
    df_solutions = load_solutions() # On garde votre base sécurisée
    
    # Transformation de la base en texte (Uniquement colonnes publiques)
    solutions_context = ""
    if not df_solutions.empty:
        for _, row in df_solutions.iterrows():
            solutions_context += f"- {row['Dénomination actuelle']} : {row['Résumé']} (Sport: {row['Sport ciblé']})\n"

    system_instructions = f"""
    Tu es l'Expert IA d'InnoRadar.
    TON PROCESSUS :
    1. Analyse l'historique pour voir quelles questions parmi les 5 du diagnostic ont été répondues.
    2. Si le diagnostic est incomplet, remercie l'utilisateur et pose la QUESTION SUIVANTE parmi : {QUESTIONS}.
    3. Si le diagnostic est terminé, propose un matchmaking basé sur :
    {solutions_context}
    
    RÈGLES D'OR :
    - Ton : Institutionnel et expert.
    - Relevance Score : Obligatoire pour chaque solution.
    - Doute : Si une solution n'est pas 100% Sport Tech, signale-le.
    """
    
    # ... Logique d'envoi Gemini ...
    
    # Construction du prompt avec historique
    history_context = ""
    for msg in history:
        role = "Utilisateur" if msg["role"] == "user" else "Assistant"
        history_context += f"{role}: {msg['content']}\n"
    
    full_prompt = f"{system_instructions}\n\n{history_context}\nUtilisateur: {prompt}\nAssistant:"
    
    response = model.generate_content(full_prompt)
    return response.text
