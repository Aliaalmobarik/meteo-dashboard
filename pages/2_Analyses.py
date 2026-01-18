import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =====================
# CONFIGURATION PAGE
# =====================
st.set_page_config(
    page_title="📈 Analyses Météo",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    [data-testid="stSidebarNav"] { display: none !important; }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f3460 0%, #1a1a2e 100%);
    }
    
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif !important;
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .main-title {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, rgba(0,210,255,0.1) 0%, rgba(58,123,213,0.1) 100%);
        border-radius: 20px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# =====================
# CHEMINS RELATIFS
# =====================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# =====================
# CHARGEMENT DONNÉES
# =====================
@st.cache_data
def load_data():
    data_path = DATA_DIR / "clean" / "meteo_clean.parquet"
    df = pd.read_parquet(data_path)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

noms_mois = {
    1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 
    5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août", 
    9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
}

# =====================
# SIDEBAR
# =====================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <span style="font-size: 3rem;">🌦️</span>
            <h2 style="margin: 10px 0; font-size: 1.5rem;">GeoMétéo</h2>
            <p style="color: #888; font-size: 0.8rem;">Analyses Temporelles</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.page_link("app.py", label="🏠 Accueil")
    st.page_link("pages/1_Carte.py", label="🗺️ Carte")
    st.page_link("pages/2_Analyses.py", label="📈 Analyses")
    st.page_link("pages/3_Comparaison.py", label="🔄 Comparaison")
    
    st.markdown("---")
    
    st.markdown("### 🗺️ Filtres")
    
    deps = sorted(df["dep"].dropna().unique())
    selected_dep = st.selectbox(
        "Département",
        ["Tous"] + list(deps),
        format_func=lambda x: "🌍 Tous" if x == "Tous" else f"📍 Dép. {x}"
    )

# =====================
# FILTRAGE
# =====================
df_filtered = df.copy()
if selected_dep != "Tous":
    df_filtered = df_filtered[df_filtered["dep"] == selected_dep]

# =====================
# PAGE PRINCIPALE
# =====================
st.markdown("""
    <div class="main-title">
        <h1>📈 Analyses Climatiques</h1>
        <p style="color: #a0a0a0;">Évolution temporelle • Tendances • Statistiques</p>
    </div>
""", unsafe_allow_html=True)

# =====================
# GRAPHIQUE 1: ÉVOLUTION TEMPÉRATURE
# =====================
st.markdown("### 🌡️ Évolution de la Température")

if len(df_filtered) > 0:
    temp_mensuelle = df_filtered.groupby(df_filtered["date"].dt.to_period("M")).agg({
        "T": "mean",
        "TX": "max",
        "TN": "min"
    }).reset_index()
    temp_mensuelle["date"] = temp_mensuelle["date"].dt.to_timestamp()
    
    fig_temp = go.Figure()
    
    fig_temp.add_trace(go.Scatter(
        x=temp_mensuelle["date"],
        y=temp_mensuelle["TX"],
        mode="lines",
        name="T Max",
        line=dict(color="#ff6b6b", width=1),
        fill=None
    ))
    
    fig_temp.add_trace(go.Scatter(
        x=temp_mensuelle["date"],
        y=temp_mensuelle["TN"],
        mode="lines",
        name="T Min",
        line=dict(color="#4ecdc4", width=1),
        fill="tonexty",
        fillcolor="rgba(0,210,255,0.2)"
    ))
    
    fig_temp.add_trace(go.Scatter(
        x=temp_mensuelle["date"],
        y=temp_mensuelle["T"],
        mode="lines+markers",
        name="T Moyenne",
        line=dict(color="#00d2ff", width=3)
    ))
    
    fig_temp.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8e8e8"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)", title="Température (°C)"),
        legend=dict(bgcolor="rgba(0,0,0,0.3)"),
        height=400
    )
    
    st.plotly_chart(fig_temp, use_container_width=True)

# =====================
# GRAPHIQUE 2: PRÉCIPITATIONS
# =====================
st.markdown("### 🌧️ Précipitations Mensuelles")

if len(df_filtered) > 0:
    precip_mensuelle = df_filtered.groupby(df_filtered["date"].dt.to_period("M"))["RR1"].sum().reset_index()
    precip_mensuelle["date"] = precip_mensuelle["date"].dt.to_timestamp()
    
    fig_precip = px.bar(
        precip_mensuelle,
        x="date",
        y="RR1",
        color="RR1",
        color_continuous_scale=[[0, "#4ecdc4"], [0.5, "#3a7bd5"], [1, "#00d2ff"]]
    )
    
    fig_precip.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8e8e8"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)", title=""),
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)", title="Précipitations (mm)"),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig_precip, use_container_width=True)

# =====================
# GRAPHIQUE 3: SAISONNALITÉ
# =====================
st.markdown("### 📅 Profil Saisonnier")

col1, col2 = st.columns(2)

if len(df_filtered) > 0:
    with col1:
        df_filtered["mois"] = df_filtered["date"].dt.month
        temp_mois = df_filtered.groupby("mois")["T"].mean().reset_index()
        temp_mois["mois_nom"] = temp_mois["mois"].map(noms_mois)
        
        fig_sais_temp = px.bar(
            temp_mois,
            x="mois_nom",
            y="T",
            color="T",
            color_continuous_scale=[[0, "#4ecdc4"], [0.5, "#ffcc00"], [1, "#ff6b6b"]]
        )
        
        fig_sais_temp.update_layout(
            title=dict(text="Température moyenne par mois", font=dict(color="#00d2ff")),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e8e8e8"),
            xaxis=dict(tickangle=45),
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_sais_temp, use_container_width=True)
    
    with col2:
        precip_mois = df_filtered.groupby("mois")["RR1"].sum().reset_index()
        precip_mois["mois_nom"] = precip_mois["mois"].map(noms_mois)
        
        fig_sais_precip = px.bar(
            precip_mois,
            x="mois_nom",
            y="RR1",
            color="RR1",
            color_continuous_scale=[[0, "#00d2ff"], [1, "#3a7bd5"]]
        )
        
        fig_sais_precip.update_layout(
            title=dict(text="Précipitations totales par mois", font=dict(color="#00d2ff")),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e8e8e8"),
            xaxis=dict(tickangle=45),
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_sais_precip, use_container_width=True)

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
    <div style="
        text-align: center;
        padding: 20px;
        background: rgba(255,255,255,0.03);
        border-radius: 15px;
    ">
        <p style="color: #666; margin: 0; font-size: 0.85rem;">
            📊 Données : <strong>Météo-France</strong> | 
            📈 <strong>Plotly</strong> |
            👩‍💻 <strong style="color: #00d2ff;">Alia AL MOBARIK</strong>
        </p>
    </div>
""", unsafe_allow_html=True)
