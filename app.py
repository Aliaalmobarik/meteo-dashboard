import streamlit as st

# =====================
# CONFIGURATION PAGE D'ACCUEIL
# =====================
st.set_page_config(
    page_title=" GeoMétéo Dashboard",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS moderne
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Cacher le menu de navigation automatique de Streamlit */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f3460 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif !important;
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }
    
    .welcome-box {
        text-align: center;
        padding: 60px 40px;
        background: linear-gradient(135deg, rgba(0,210,255,0.1) 0%, rgba(58,123,213,0.1) 100%);
        border-radius: 30px;
        border: 1px solid rgba(255,255,255,0.1);
        margin: 40px 0;
    }
    
    .welcome-box h1 {
        font-size: 3.5rem !important;
        margin-bottom: 20px !important;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 210, 255, 0.2);
        border-color: rgba(0, 210, 255, 0.3);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    
    .feature-title {
        color: #00d2ff;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .feature-desc {
        color: #a0a0a0;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# =====================
# SIDEBAR
# =====================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <span style="font-size: 4rem;">🌦️</span>
            <h2 style="margin: 15px 0; font-size: 1.8rem;">GeoMétéo</h2>
            <p style="color: #888; font-size: 0.9rem;">Dashboard Météo - Géodatavisualisation</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation personnalisée
    st.markdown("""
        <p style="color: #00d2ff; font-size: 0.9rem; margin-bottom: 15px; padding-left: 10px;">📍 Navigation</p>
    """, unsafe_allow_html=True)
    
    st.page_link("app.py", label="🏠 Accueil", icon=None)
    st.page_link("pages/1_Carte.py", label="🗺️ Carte", icon=None)
    st.page_link("pages/2_Analyses.py", label="📈 Analyses", icon=None)
    st.page_link("pages/3_Comparaison.py", label="🔄 Comparaison", icon=None)

# =====================
# CONTENU PRINCIPAL
# =====================

# Titre de bienvenue
st.markdown("""
    <div class="welcome-box">
        <h1>🌦️ GeoMétéo Dashboard</h1>
        <p style="color: #a0a0a0; font-size: 1.3rem; margin: 0;">
            Observatoire Météorologique Spatio-temporel
        </p>
        <p style="color: #666; font-size: 1rem; margin-top: 15px;">
            Données Météo-France • Projet Géodata-visualisation 
        </p>
    </div>
""", unsafe_allow_html=True)

# Fonctionnalités
st.markdown("### 🚀 Fonctionnalités")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌍</div>
            <div class="feature-title">Carte Interactive</div>
            <div class="feature-desc">
                Visualisation spatiale des données météorologiques avec heatmaps 
                de température et précipitations. Filtres par département et période.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Analyses Climatiques</div>
            <div class="feature-desc">
                Graphiques d'évolution temporelle : température, précipitations, 
                humidité et rose des vents. Statistiques détaillées.
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Données disponibles
st.markdown("### 📊 Données Disponibles")

col3, col4, col5, col6 = st.columns(4)

with col3:
    st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(255,107,107,0.1); border-radius: 15px; border: 1px solid rgba(255,107,107,0.2);">
            <span style="font-size: 2rem;">🌡️</span>
            <p style="color: #ff6b6b; font-weight: 600; margin: 10px 0 5px 0;">Température</p>
            <p style="color: #888; font-size: 0.8rem; margin: 0;">T, TX, TN</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(78,205,196,0.1); border-radius: 15px; border: 1px solid rgba(78,205,196,0.2);">
            <span style="font-size: 2rem;">🌧️</span>
            <p style="color: #4ecdc4; font-weight: 600; margin: 10px 0 5px 0;">Précipitations</p>
            <p style="color: #888; font-size: 0.8rem; margin: 0;">RR1 (mm)</p>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(102,126,234,0.1); border-radius: 15px; border: 1px solid rgba(102,126,234,0.2);">
            <span style="font-size: 2rem;">💧</span>
            <p style="color: #667eea; font-weight: 600; margin: 10px 0 5px 0;">Humidité</p>
            <p style="color: #888; font-size: 0.8rem; margin: 0;">U (%)</p>
        </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(0,210,255,0.1); border-radius: 15px; border: 1px solid rgba(0,210,255,0.2);">
            <span style="font-size: 2rem;">💨</span>
            <p style="color: #00d2ff; font-weight: 600; margin: 10px 0 5px 0;">Vent</p>
            <p style="color: #888; font-size: 0.8rem; margin: 0;">FF, DD</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="
        text-align: center;
        padding: 25px;
        background: rgba(255,255,255,0.03);
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.05);
    ">
        <p style="color: #666; margin: 0; font-size: 0.9rem;">
            🎓 <strong>Projet M2 GMS</strong> | 
            💾 Données <strong>Météo-France</strong> | 
            🛠️ Streamlit, Folium, Plotly
            👩‍💻 <strong style="color: #00d2ff;">Alia AL MOBARIK</strong>
        </p>
    </div>
""", unsafe_allow_html=True)
