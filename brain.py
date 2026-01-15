import pandas as pd
import streamlit as st

def load_solutions():
    try:
        df = pd.read_csv("solutions.csv")
        
        # LISTE BLANCHE : Uniquement les colonnes non-sensibles
        # Tout ce qui est Email, CA, Levée de fonds, Contact est EXCLU
        cols_publiques = [
            "Dénomination actuelle", 
            "Type d'innovation", 
            "Type de produits / services", 
            "Sport ciblé", 
            "Type d’utilisateurs",
            "Clientèle cible", 
            "Résumé", 
            "Cas d'usage", 
            "Statut de la solution",
            "Catégorisation",
            "Caractéristiques clés / proposition de valeur",
            "Site internet"
        ]
        
        # On ne garde que ces colonnes
        df_public = df[cols_publiques].fillna("Non renseigné")
        return df_public
    except Exception as e:
        st.error(f"Erreur lors du chargement sécurisé : {e}")
        return pd.DataFrame()

def generate_response(model, prompt, history):
    df_solutions = load_solutions()
    
    # On transforme les données en texte pour l'IA (format compact)
    solutions_context = ""
    for _, row in df_solutions.iterrows():
        solutions_context += f"- {row['Dénomination actuelle']} : {row['Résumé']} (Sport: {row['Sport ciblé']}, Usage: {row['Cas d'usage']})\n"

    system_instructions = f"""
    Tu es l'intelligence centrale d'InnoRadar.
    TON RÔLE : Matchmaking B2B Sport Tech.
    
    BASE DE DONNÉES AUTORISÉE :
    {solutions_context}
    
    CONSIGNES DE SÉCURITÉ :
    1. Tu n'as accès qu'aux descriptions publiques des solutions. 
    2. Ne spécule jamais sur les finances, les emails ou les données privées.
    3. Si l'utilisateur pose une question d'ordre financier ou privé, réponds que ces données sont confidentielles et ne sont pas traitées par cette interface.
    4. Pour chaque suggestion, indique le 'Relevance Score' (%).
    """
    
    # Appel au modèle
    full_prompt = f"{system_instructions}\n\nQuestions précédentes:\n{history}\n\nUtilisateur: {prompt}"
    response = model.generate_content(full_prompt)
    
    return response.text
