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

def generate_response(model, prompt, history):
    df_solutions = load_solutions()
    
    # Transformation des solutions en texte pour l'IA
    if not df_solutions.empty:
        solutions_text = ""
        for _, row in df_solutions.iterrows():
            solutions_text += f"- {row['Dénomination actuelle']} : {row['Résumé']} (Sport: {row['Sport ciblé']})\n"
    else:
        solutions_text = "Aucune donnée disponible."

    system_instructions = f"""
    Tu es l'intelligence centrale d'InnoRadar.
    
    BASE DE DONNÉES DISPONIBLE :
    {solutions_text}
    
    CONSIGNES :
    1. Aide l'utilisateur à trouver la meilleure solution Sport Tech.
    2. Utilise un ton professionnel et expert.
    3. RELEVANCE SCORE : Attribue un score de 0 à 100% pour chaque recommandation.
    4. SÉCURITÉ : Ne mentionne jamais de données financières ou privées.
    5. DOUTE : Si tu doutes du lien entre une solution et le sport, signale-le explicitement.
    """
    
    # Construction du prompt avec historique
    history_context = ""
    for msg in history:
        role = "Utilisateur" if msg["role"] == "user" else "Assistant"
        history_context += f"{role}: {msg['content']}\n"
    
    full_prompt = f"{system_instructions}\n\n{history_context}\nUtilisateur: {prompt}\nAssistant:"
    
    response = model.generate_content(full_prompt)
    return response.text
