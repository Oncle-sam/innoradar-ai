import streamlit as st
from styles import apply_styles
from brain import get_model, generate_response

# Configuration
st.set_page_config(page_title="Innoradar", page_icon="🚀", layout="wide")
apply_styles()

st.title("InnoRadar")
st.write("L'outil IA de matchmaking parfait connectant les acteurs du sport aux innovations vraiment utiles.")


import streamlit as st

st.set_page_config(page_title="InnoRadar", page_icon="🎯", layout="wide")

# Injection de l'identité visuelle (Violet & Void)
st.markdown("""
    <style>
    /* Fond principal */
    .stApp {
        background-color: #0f1025;
        color: #f8fafc;
    }
    /* Style des questions de l'IA (Bulles) */
    .stChatMessage {
        background: rgba(26, 27, 59, 0.6) !important;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
    }
    /* Titre InnoRadar */
    .main-title {
        font-family: 'Exo 2', sans-serif;
        font-weight: 800;
        background: linear-gradient(90deg, #8b5cf6, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
    }
    </style>
    <h1 class="main-title">INNORADAR</h1>
    """, unsafe_allow_html=True)

# Initialisation du modèle
try:
# Modifiez cette ligne pour "déballer" le tuple
    model, model_name = get_model()

# Optionnel : affichez le modèle actif dans la sidebar pour confirmer que ça marche
    st.sidebar.success(f"IA connectée : {model_name}")
except Exception as e:
    st.error(f"Erreur de connexion à l'IA : {e}")
    st.stop()

# Gestion du Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Posez votre question à InnoRadar..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = generate_response(model, prompt, st.session_state.messages)
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})


# 3. Affichage de la barre latérale (FilterBar)
filters = render_filter_bar(df)

# 4. Affichage du formulaire principal (MatchForm)
search_params = render_match_form()

# 5. Logique de Matchmaking (Le moteur)
if search_params["submit"] or search_params["query"]:
    # Filtrage du DataFrame en fonction des choix de l'utilisateur
    results = df.copy()
    
    if search_params["category"] != "Toutes":
        results = results[results['Catégorisation'] == search_params["category"]]
        
    if search_params["innovation"] != "Toutes":
        results = results[results["Type d'innovation"].str.contains(search_params["innovation"], na=False)]
    
    if search_params["query"]:
        results = results[results['Résumé'].str.contains(search_params["query"], case=False, na=False)]

    # Affichage des résultats
    st.markdown(f"### 📊 {len(results)} Solutions trouvées")
    
    for _, row in results.iterrows():
        with st.container():
            st.markdown(f"""
            <div style="background: rgba(26, 27, 59, 0.4); padding: 20px; border-radius: 10px; border-left: 5px solid #8b5cf6; margin-bottom: 10px;">
                <h4 style="color: #60a5fa; margin: 0;">{row['Dénomination actuelle']}</h4>
                <p style="font-size: 0.9rem; color: #cbd5e1;">{row['Résumé']}</p>
                <span style="background: #8b5cf6; padding: 2px 8px; border-radius: 5px; font-size: 0.7rem;">{row['Sport ciblé']}</span>
            </div>
            """, unsafe_allow_html=True)
