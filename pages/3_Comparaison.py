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
    page_title="🔄 Comparaison Départements",
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
    
    .dept-card {
        background: rgba(0, 210, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(0, 210, 255, 0.2);
        text-align: center;
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

DEPT_NOMS = {
    "04": "Alpes-de-Haute-Provence",
    "05": "Hautes-Alpes",
    "06": "Alpes-Maritimes",
    "13": "Bouches-du-Rhône",
    "83": "Var",
    "84": "Vaucluse"
}

dept_colors = {
    "04": "#ff6b6b",
    "05": "#4ecdc4",
    "06": "#45b7d1",
    "13": "#96ceb4",
    "83": "#feca57",
    "84": "#ff9ff3"
}

# =====================
# SIDEBAR
# =====================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <span style="font-size: 3rem;">🌦️</span>
            <h2 style="margin: 10px 0; font-size: 1.5rem;">GeoMétéo</h2>
            <p style="color: #888; font-size: 0.8rem;">Comparaison Départements</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.page_link("app.py", label="🏠 Accueil")
    st.page_link("pages/1_Carte.py", label="🗺️ Carte")
    st.page_link("pages/2_Analyses.py", label="📈 Analyses")
    st.page_link("pages/3_Comparaison.py", label="🔄 Comparaison")
    
    st.markdown("---")
    
    st.markdown("### 📍 Départements")
    
    all_deps = sorted(df["dep"].dropna().unique().tolist())
    selected_deps = st.multiselect(
        "Sélectionner",
        options=all_deps,
        default=all_deps,
        format_func=lambda x: f"📍 {x} - {DEPT_NOMS.get(x, x)}"
    )

# =====================
# FILTRAGE
# =====================
df_filtered = df[df["dep"].isin(selected_deps)]

# =====================
# PAGE PRINCIPALE
# =====================
st.markdown("""
    <div class="main-title">
        <h1>🔄 Comparaison Inter-Départementale</h1>
        <p style="color: #a0a0a0;">Analyse comparative • Statistiques • Tendances</p>
    </div>
""", unsafe_allow_html=True)

# =====================
# CARTES DE SYNTHÈSE
# =====================
st.markdown("### 📊 Bilan par Département")

if len(df_filtered) > 0:
    dept_stats = df_filtered.groupby("dep").agg({
        "T": "mean",
        "RR1": "sum",
        "U": "mean"
    }).reset_index()
    
    cols = st.columns(min(len(selected_deps), 6))
    
    for i, dep in enumerate(selected_deps[:6]):
        with cols[i % len(cols)]:
            dep_data = dept_stats[dept_stats["dep"] == dep]
            if len(dep_data) > 0:
                temp = dep_data["T"].values[0]
                precip = dep_data["RR1"].values[0]
                nom = DEPT_NOMS.get(dep, dep)
                
                st.markdown(f"""
                    <div class="dept-card">
                        <h4 style="color: #00d2ff; margin: 10px 0;">{dep} - {nom}</h4>
                        <p style="color: #ff6b6b; font-size: 1.5rem; font-weight: 700; margin: 5px 0;">{temp:.1f}°C</p>
                        <p style="color: #888; font-size: 0.8rem; margin: 0;">T moyenne</p>
                        <p style="color: #4ecdc4; font-size: 1.2rem; font-weight: 600; margin: 10px 0 5px 0;">{precip:,.0f} mm</p>
                        <p style="color: #888; font-size: 0.8rem; margin: 0;">Précipitations</p>
                    </div>
                """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================
# GRAPHIQUE 1: COMPARAISON TEMPÉRATURES
# =====================
st.markdown("### 🌡️ Comparaison des Températures")

if len(df_filtered) > 0:
    temp_dept = df_filtered.groupby(["dep", df_filtered["date"].dt.to_period("M")])["T"].mean().reset_index()
    temp_dept["date"] = temp_dept["date"].dt.to_timestamp()
    
    fig_temp = px.line(
        temp_dept,
        x="date",
        y="T",
        color="dep",
        color_discrete_map=dept_colors,
        labels={"T": "Température (°C)", "date": "", "dep": "Département"}
    )
    
    fig_temp.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8e8e8"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
        legend=dict(bgcolor="rgba(0,0,0,0.3)"),
        height=400
    )
    
    st.plotly_chart(fig_temp, use_container_width=True)

# =====================
# GRAPHIQUE 2: COMPARAISON PRÉCIPITATIONS
# =====================
st.markdown("### 🌧️ Comparaison des Précipitations")

if len(df_filtered) > 0:
    precip_dept = df_filtered.groupby("dep")["RR1"].sum().reset_index()
    precip_dept = precip_dept.sort_values("RR1", ascending=True)
    precip_dept["nom"] = precip_dept["dep"].map(DEPT_NOMS)
    
    fig_precip = px.bar(
        precip_dept,
        x="RR1",
        y="dep",
        orientation="h",
        color="RR1",
        color_continuous_scale=[[0, "#4ecdc4"], [1, "#00d2ff"]],
        text="RR1"
    )
    
    fig_precip.update_traces(
        texttemplate='%{text:,.0f} mm',
        textposition='outside',
        textfont=dict(color="#e8e8e8")
    )
    
    fig_precip.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8e8e8"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)", title="Précipitations (mm)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)", title=""),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig_precip, use_container_width=True)

# =====================
# GRAPHIQUE 3: RADAR
# =====================
st.markdown("### 🎯 Profil Climatique")

if len(df_filtered) > 0 and len(selected_deps) >= 2:
    dept_profile = df_filtered.groupby("dep").agg({
        "T": "mean",
        "TX": "max",
        "TN": "min",
        "RR1": "sum",
        "U": "mean"
    }).reset_index()
    
    # Normalisation
    for col in ["T", "TX", "TN", "RR1", "U"]:
        max_val = dept_profile[col].max()
        dept_profile[f"{col}_norm"] = dept_profile[col] / max_val if max_val > 0 else 0
    
    fig_radar = go.Figure()
    
    categories = ['T Moy', 'T Max', 'T Min', 'Précip', 'Humidité']
    
    for dep in selected_deps[:4]:
        dep_data = dept_profile[dept_profile["dep"] == dep]
        if len(dep_data) > 0:
            values = [
                dep_data["T_norm"].values[0],
                dep_data["TX_norm"].values[0],
                dep_data["TN_norm"].values[0],
                dep_data["RR1_norm"].values[0],
                dep_data["U_norm"].values[0]
            ]
            values.append(values[0])
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name=f"{dep} - {DEPT_NOMS.get(dep, dep)}",
                line=dict(color=dept_colors.get(dep, "#00d2ff"))
            ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="rgba(255,255,255,0.2)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.2)"),
            bgcolor="rgba(0,0,0,0)"
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8e8e8"),
        legend=dict(bgcolor="rgba(0,0,0,0.3)"),
        height=500
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)

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
            🔄 <strong>6 départements PACA</strong> |
            👩‍💻 <strong style="color: #00d2ff;">Alia AL MOBARIK</strong>
        </p>
    </div>
""", unsafe_allow_html=True)
