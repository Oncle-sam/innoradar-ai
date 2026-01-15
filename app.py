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

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=SYSTEM_PROMPT
)

# --- INTERFACE UTILISATEUR ---
st.set_page_config(page_title="Innoradar", page_icon="🚀")

st.title("🚀InnoRadar")
st.write("L'outil IA de matchmaking parfait connectant les acteurs du sport aux innovations vraiment utiles.")

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