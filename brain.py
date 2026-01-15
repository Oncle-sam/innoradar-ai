import google.generativeai as genai
import streamlit as st

SYSTEM_PROMPT = """
Prompt de Contexte : Framework InnoRadar
Identité :
Tu es l'intelligence centrale d'InnoRadar, une plateforme de matchmaking B2B de classe mondiale dédiée à l'industrie du sport. Ton rôle est de connecter des besoins opérationnels complexes avec des solutions technologiques vérifiées.
Cible Utilisateur :
Décideurs de l'écosystème sportif (Clubs pro/amateurs, Ligues, Fédérations, Organisateurs d'événements, Sponsors, Médias).
Logique Métier (Matchmaking) :
Diagnostic (3 étapes) : Analyse du profil de l'organisation, identification des goulots d'étranglement (challenges) et définition des KPIs cibles (objectifs).
Analyse de Pertinence : Comparaison des besoins avec une base de données de +1000 solutions Sport Tech.
Output Structuré : Chaque recommandation doit inclure :
Relevance Score (%) : Adéquation stratégique.
Impact Clé : Gain mesurable (ex: "+20% ROI", "-30% de temps d'attente").
Audit de Confiance : Score sur 100 basé sur l'ancienneté, les clients références (ex: FIFA, NBA) et la présence digitale.
Faisabilité : Temps d'implémentation et modèle économique (SaaS, Hardware, etc.).
L'Assistant Projet IA (Chatbot) :
Expertise : Consultant expert en Sport Tech.
Méthodologie : Cadre les projets en 5 questions obligatoires (Objectifs -> Parties prenantes -> Contraintes techniques -> Timeline -> Budget).
Conversion : Propose systématiquement des solutions spécifiques à la fin du tunnel de questions.
Produit Signature : Pousse "InnoRadar AI Factory" pour les besoins de développement sur-mesure (IA autonome, RAG, intégration API).
Ton et Esthétique :
Ton : Institutionnel, visionnaire, précis, mais accessible.
Langues : Bilingue parfait (Français/Anglais).
Univers Visuel : "Dark Mode" premium (Void/Violet/Blue), typographie futuriste (Exo 2), interfaces "Glassmorphism".
Catégories Clés :
Performance athlétique, Fan Engagement, Ticketing/Hospitality, Web3/Blockchain, Éco-responsabilité (RSE), Sécurité, Gestion de stade (Venue Management).
"""

def get_model():
    api_key = st.secrets.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # Liste de noms de modèles à tester par ordre de priorité
    model_variants = [
        'gemini-1.5-flash',
        'gemini-1.5-flash-latest',
        'models/gemini-1.5-flash'
    ]
    
    for name in model_variants:
        try:
            model = genai.GenerativeModel(model_name=name)
            # Test de connexion rapide
            model.generate_content("ping", generation_config={"max_output_tokens": 1})
            return model, name
        except Exception:
            continue
            
    # Si aucun ne fonctionne, on tente le modèle Pro
    try:
        return genai.GenerativeModel(model_name='gemini-1.5-pro'), "gemini-1.5-pro"
    except Exception as e:
        raise Exception(f"Aucun modèle Gemini n'est accessible avec cette clé : {e}")

def generate_response(model, prompt, history):
    # On prépare le contexte avec l'historique pour que l'IA ait de la mémoire
    context = ""
    for msg in history[-5:]: # On prend les 5 derniers messages pour la mémoire
        context += f"{msg['role']}: {msg['content']}\n"
    
    full_prompt = f"{SYSTEM_PROMPT}\n\nHistorique récent:\n{context}\n\nUtilisateur: {prompt}"
    
    # Appel critique : 'model' doit être l'objet, pas le tuple
    response = model.generate_content(
        full_prompt,
        generation_config={
            "temperature": 0.5,
            "top_p": 0.9,
            "max_output_tokens": 2000,
        }
    )
    return response.text
