# ui_components.py
import streamlit as st
from constants import SOLUTIONS_CATEGORIES, INNOVATIONS

def render_match_form():
    """Équivalent de MatchForm.tsx : Le formulaire de recherche principal"""
    with st.container():
        st.markdown('<p style="color:#8b5cf6; font-weight:bold;">🎯 RECHERCHE RAPIDE</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Catégorie Métier", ["Toutes"] + SOLUTIONS_CATEGORIES)
        with col2:
            innovation = st.selectbox("Type d'Innovation", ["Toutes"] + INNOVATIONS)
            
        search_query = st.text_input("Rechercher un mot-clé (ex: Performance, Stade...)", "")
        
        submit = st.button("Lancer le Matchmaking ⚡", use_container_width=True)
        return {"category": category, "innovation": innovation, "query": search_query, "submit": submit}

def render_filter_bar(df):
    """Équivalent de FilterBar.tsx : Filtres latéraux pour affiner les résultats du CSV"""
    st.sidebar.markdown("### 🔍 FILTRES AVANCÉS")
    
    # Filtrage par Sport (dynamique selon votre CSV)
    if 'Sport ciblé' in df.columns:
        sports = df['Sport ciblé'].unique().tolist()
        selected_sport = st.sidebar.multiselect("Sports", sports)
    else:
        selected_sport = []

    # Filtrage par Stade de développement
    if 'Stade de développement' in df.columns:
        stades = df['Stade de développement'].unique().tolist()
        selected_stade = st.sidebar.multiselect("Maturité", stades)
    else:
        selected_stade = []

    return {"sports": selected_sport, "stades": selected_stade}
