import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =====================
# CONFIGURATION PAGE
# =====================
st.set_page_config(
    page_title="Comparaison Départements",
    page_icon="🔄",
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
    
    .main-title {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, rgba(0,210,255,0.1) 0%, rgba(58,123,213,0.1) 100%);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 30px;
    }
    
    .main-title h1 {
        font-size: 2.5rem !important;
        margin: 0 !important;
    }
    
    .comparison-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# =====================
# CHARGEMENT DONNÉES
# =====================
@st.cache_data
def load_data():
    df = pd.read_parquet("data/clean/meteo_clean.parquet")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# Dictionnaire mois
noms_mois = {
    1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 
    5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août", 
    9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
}

noms_mois_emoji = {
    1: "🌨️ Janvier", 2: "❄️ Février", 3: "🌱 Mars", 4: "🌷 Avril", 
    5: "🌸 Mai", 6: "☀️ Juin", 7: "🌞 Juillet", 8: "🏖️ Août", 
    9: "🍂 Septembre", 10: "🍁 Octobre", 11: "🌧️ Novembre", 12: "⛄ Décembre"
}

# Liste des départements
departements = sorted(df["DEPARTEMENT"].dropna().unique())

# =====================
# SIDEBAR
# =====================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <span style="font-size: 3rem;">🌦️</span>
            <h2 style="margin: 10px 0; font-size: 1.5rem;">GeoMétéo</h2>
            <p style="color: #888; font-size: 0.8rem;">Dashboard M2 GMS</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation personnalisée
    st.markdown("""
        <p style="color: #00d2ff; font-size: 0.9rem; margin-bottom: 15px; padding-left: 5px;">📍 Navigation</p>
    """, unsafe_allow_html=True)
    
    st.page_link("app.py", label="🏠 Accueil")
    st.page_link("pages/1_Carte.py", label="🗺️ Carte")
    st.page_link("pages/2_Analyses.py", label="📈 Analyses")
    st.page_link("pages/3_Comparaison.py", label="🔄 Comparaison")
    
    st.markdown("---")
    
    st.markdown("### 📍 Sélection des départements")
    
    # Sélection multiple de départements
    selected_deps = st.multiselect(
        "Départements à comparer",
        options=departements,
        default=departements[:3] if len(departements) >= 3 else departements,
        format_func=lambda x: f"📍 {x}"
    )
    
    st.markdown("---")
    
    st.markdown("### 📅 Période d'analyse")
    
    # Sélection de l'année
    annees = sorted(df["annee"].unique().astype(int))
    selected_year = st.select_slider(
        "Année",
        options=annees,
        value=int(df["annee"].max())
    )
    
    # Sélection du mois (optionnel)
    month = st.selectbox(
        "Mois (optionnel)",
        options=["Tous"] + list(range(1, 13)),
        index=0,
        format_func=lambda x: "📆 Tous les mois" if x == "Tous" else noms_mois_emoji.get(x, str(x))
    )
    
    st.markdown("---")
    st.markdown("""
        <div style="
            background: rgba(0,210,255,0.1);
            border-radius: 15px;
            padding: 15px;
            border: 1px solid rgba(0,210,255,0.2);
            text-align: center;
        ">
            <p style="color: #00d2ff; margin: 0; font-size: 0.85rem;">
                📊 Sélectionnez au moins 2 départements
            </p>
        </div>
    """, unsafe_allow_html=True)

# =====================
# FILTRAGE
# =====================
df_filtered = df[df["annee"] == selected_year].copy()
if month != "Tous":
    df_filtered = df_filtered[df_filtered["mois"] == month]

# Convertir DEPARTEMENT en string pour éviter le tri numérique
df_filtered["DEPARTEMENT"] = df_filtered["DEPARTEMENT"].astype(str)

# Filtrer par départements sélectionnés (convertir en string aussi)
selected_deps_str = [str(d) for d in selected_deps]
df_compare = df_filtered[df_filtered["DEPARTEMENT"].isin(selected_deps_str)]

# =====================
# TITRE
# =====================
st.markdown("""
    <div class="main-title">
        <h1>🔄 Comparaison Inter-Départementale</h1>
        <p style="color: #a0a0a0;">Analyse comparative des données météorologiques</p>
    </div>
""", unsafe_allow_html=True)

# Contexte
mois_label = "Année complète" if month == "Tous" else noms_mois.get(month, month)
deps_label = ", ".join([str(d) for d in selected_deps]) if len(selected_deps) <= 3 else f"{len(selected_deps)} départements"
st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, rgba(0,210,255,0.15) 0%, rgba(58,123,213,0.15) 100%);
        border-radius: 15px;
        padding: 15px 25px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
        text-align: center;
    ">
        <span style="color: #e8e8e8;">📍 <strong style="color: #00d2ff;">{deps_label}</strong> | 
        📅 <strong style="color: #00d2ff;">{selected_year}</strong> | 
        🗓️ <strong style="color: #00d2ff;">{mois_label}</strong></span>
    </div>
""", unsafe_allow_html=True)

# Vérification qu'au moins 2 départements sont sélectionnés
if len(selected_deps) < 2:
    st.warning("⚠️ Veuillez sélectionner au moins 2 départements pour la comparaison.")
    st.stop()

# =====================
# TABLEAU RÉCAPITULATIF
# =====================
st.markdown("### 📋 Tableau Comparatif")

# Calculer les statistiques par département
stats = []
for dep in selected_deps_str:
    dep_data = df_compare[df_compare["DEPARTEMENT"] == dep]
    precip_total = dep_data.groupby("NUM_POSTE")["RR1"].sum().mean()
    stats.append({
        "Département": dep,
        "🌡️ T° Moy (°C)": round(dep_data["T"].mean(), 1),
        "🌡️ T° Max (°C)": round(dep_data["T"].max(), 1),
        "🌡️ T° Min (°C)": round(dep_data["T"].min(), 1),
        "🌧️ Précip (mm)": round(precip_total, 1),
        "💧 Humid (%)": round(dep_data["U"].mean(), 1),
        "💨 Vent (m/s)": round(dep_data["FF"].mean(), 1),
    })

df_stats = pd.DataFrame(stats)
st.dataframe(df_stats, use_container_width=True, hide_index=True)

# =====================
# GRAPHIQUES COMPARATIFS
# =====================
st.markdown("### 📊 Comparaison Température")

col1, col2 = st.columns(2)

# --- Bar Chart Température Moyenne ---
with col1:
    temp_by_dep = df_compare.groupby("DEPARTEMENT")["T"].mean().reset_index()
    temp_by_dep = temp_by_dep.sort_values("T", ascending=False)
    
    fig_temp_bar = px.bar(
        temp_by_dep,
        x="DEPARTEMENT",
        y="T",
        color="T",
        color_continuous_scale=["#3a7bd5", "#00d2ff", "#ffd700", "#ff6b6b"],
        title="🌡️ Température moyenne par département"
    )
    fig_temp_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Département",
        yaxis_title="Température (°C)",
        font=dict(family="Poppins", color="#e8e8e8"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_temp_bar, use_container_width=True)

# --- Évolution mensuelle comparée ---
with col2:
    if month == "Tous":
        temp_monthly = df_compare.groupby(["mois", "DEPARTEMENT"])["T"].mean().reset_index()
        temp_monthly["mois_nom"] = temp_monthly["mois"].map(noms_mois)
        
        fig_temp_line = px.line(
            temp_monthly,
            x="mois_nom",
            y="T",
            color="DEPARTEMENT",
            markers=True,
            title="🌡️ Évolution mensuelle comparée"
        )
        fig_temp_line.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="",
            yaxis_title="Température (°C)",
            font=dict(family="Poppins", color="#e8e8e8"),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            legend=dict(title="Département", bgcolor='rgba(0,0,0,0.3)')
        )
        st.plotly_chart(fig_temp_line, use_container_width=True)
    else:
        # Box plot pour un mois spécifique
        fig_temp_box = px.box(
            df_compare,
            x="DEPARTEMENT",
            y="T",
            color="DEPARTEMENT",
            title=f"🌡️ Distribution des températures ({noms_mois[month]})"
        )
        fig_temp_box.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Département",
            yaxis_title="Température (°C)",
            font=dict(family="Poppins", color="#e8e8e8"),
            showlegend=False
        )
        st.plotly_chart(fig_temp_box, use_container_width=True)

# =====================
# PRÉCIPITATIONS
# =====================
st.markdown("### 🌧️ Comparaison Précipitations")

col3, col4 = st.columns(2)

# --- Bar Chart Précipitations ---
with col3:
    precip_by_dep = df_compare.groupby(["DEPARTEMENT", "NUM_POSTE"])["RR1"].sum().reset_index()
    precip_by_dep = precip_by_dep.groupby("DEPARTEMENT")["RR1"].mean().reset_index()
    precip_by_dep = precip_by_dep.sort_values("RR1", ascending=False)
    
    fig_precip_bar = px.bar(
        precip_by_dep,
        x="DEPARTEMENT",
        y="RR1",
        color="RR1",
        color_continuous_scale=["#e0f7fa", "#4dd0e1", "#0097a7", "#006064"],
        title="🌧️ Précipitations cumulées par département"
    )
    fig_precip_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Département",
        yaxis_title="Précipitations (mm)",
        font=dict(family="Poppins", color="#e8e8e8"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_precip_bar, use_container_width=True)

# --- Évolution mensuelle précipitations ---
with col4:
    if month == "Tous":
        precip_monthly = df_compare.groupby(["mois", "DEPARTEMENT", "NUM_POSTE"])["RR1"].sum().reset_index()
        precip_monthly = precip_monthly.groupby(["mois", "DEPARTEMENT"])["RR1"].mean().reset_index()
        precip_monthly["mois_nom"] = precip_monthly["mois"].map(noms_mois)
        
        fig_precip_line = px.bar(
            precip_monthly,
            x="mois_nom",
            y="RR1",
            color="DEPARTEMENT",
            barmode="group",
            title="🌧️ Précipitations mensuelles comparées"
        )
        fig_precip_line.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="",
            yaxis_title="Précipitations (mm)",
            font=dict(family="Poppins", color="#e8e8e8"),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            legend=dict(title="Département", bgcolor='rgba(0,0,0,0.3)')
        )
        st.plotly_chart(fig_precip_line, use_container_width=True)
    else:
        # Box plot précipitations
        fig_precip_box = px.box(
            df_compare,
            x="DEPARTEMENT",
            y="RR1",
            color="DEPARTEMENT",
            title=f"🌧️ Distribution des précipitations ({noms_mois[month]})"
        )
        fig_precip_box.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Département",
            yaxis_title="Précipitations (mm)",
            font=dict(family="Poppins", color="#e8e8e8"),
            showlegend=False
        )
        st.plotly_chart(fig_precip_box, use_container_width=True)

# =====================
# RADAR CHART MULTI-VARIABLES
# =====================
st.markdown("### 🎯 Profil Climatique Comparé")

# Normaliser les données pour le radar chart
def normalize(series):
    min_val = series.min()
    max_val = series.max()
    if max_val - min_val == 0:
        return series * 0 + 0.5
    return (series - min_val) / (max_val - min_val)

# Calculer les moyennes par département
radar_data = []
for dep in selected_deps_str:
    dep_data = df_compare[df_compare["DEPARTEMENT"] == dep]
    precip = dep_data.groupby("NUM_POSTE")["RR1"].sum().mean()
    radar_data.append({
        "Département": dep,
        "Température": dep_data["T"].mean(),
        "Précipitations": precip,
        "Humidité": dep_data["U"].mean(),
        "Vent": dep_data["FF"].mean(),
        "Pression": dep_data["PMER"].mean()
    })

df_radar = pd.DataFrame(radar_data)

# Normaliser
for col in ["Température", "Précipitations", "Humidité", "Vent", "Pression"]:
    df_radar[f"{col}_norm"] = normalize(df_radar[col])

# Créer le radar chart
categories = ["Température", "Précipitations", "Humidité", "Vent", "Pression"]
fig_radar = go.Figure()

# Couleurs prédéfinies pour le radar
radar_colors = [
    ("#00d2ff", "rgba(0, 210, 255, 0.2)"),
    ("#ff6b6b", "rgba(255, 107, 107, 0.2)"),
    ("#4ecdc4", "rgba(78, 205, 196, 0.2)"),
    ("#ffd700", "rgba(255, 215, 0, 0.2)"),
    ("#9b59b6", "rgba(155, 89, 182, 0.2)"),
    ("#e74c3c", "rgba(231, 76, 60, 0.2)"),
]

for i, dep in enumerate(selected_deps_str):
    dep_row = df_radar[df_radar["Département"] == dep].iloc[0]
    values = [dep_row[f"{cat}_norm"] for cat in categories]
    values.append(values[0])  # Fermer le polygone
    
    color_idx = i % len(radar_colors)
    line_color, fill_color = radar_colors[color_idx]
    
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories + [categories[0]],
        fill='toself',
        name=str(dep),
        line=dict(color=line_color, width=2),
        fillcolor=fill_color
    ))

fig_radar.update_layout(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Poppins", color="#e8e8e8"),
    polar=dict(
        bgcolor='rgba(0,0,0,0)',
        radialaxis=dict(
            visible=True,
            range=[0, 1],
            gridcolor='rgba(255,255,255,0.1)',
            linecolor='rgba(255,255,255,0.1)'
        ),
        angularaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            linecolor='rgba(255,255,255,0.1)'
        )
    ),
    legend=dict(
        title="Département",
        bgcolor='rgba(0,0,0,0.3)',
        bordercolor='rgba(255,255,255,0.1)'
    ),
    title="🎯 Profil climatique normalisé"
)

st.plotly_chart(fig_radar, use_container_width=True)

# =====================
# ÉVOLUTION ANNUELLE COMPARÉE
# =====================
st.markdown("### 📅 Évolution Annuelle Comparée")

col5, col6 = st.columns(2)

# Données toutes années pour les départements sélectionnés
df_annual = df.copy()
df_annual["DEPARTEMENT"] = df_annual["DEPARTEMENT"].astype(str)
df_annual = df_annual[df_annual["DEPARTEMENT"].isin(selected_deps_str)]

with col5:
    temp_annual = df_annual.groupby(["annee", "DEPARTEMENT"])["T"].mean().reset_index()
    
    fig_temp_annual = px.line(
        temp_annual,
        x="annee",
        y="T",
        color="DEPARTEMENT",
        markers=True,
        title="🌡️ Température moyenne annuelle"
    )
    fig_temp_annual.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Année",
        yaxis_title="Température (°C)",
        font=dict(family="Poppins", color="#e8e8e8"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', dtick=1),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        legend=dict(title="Département", bgcolor='rgba(0,0,0,0.3)')
    )
    st.plotly_chart(fig_temp_annual, use_container_width=True)

with col6:
    precip_annual = df_annual.groupby(["annee", "DEPARTEMENT", "NUM_POSTE"])["RR1"].sum().reset_index()
    precip_annual = precip_annual.groupby(["annee", "DEPARTEMENT"])["RR1"].mean().reset_index()
    
    fig_precip_annual = px.line(
        precip_annual,
        x="annee",
        y="RR1",
        color="DEPARTEMENT",
        markers=True,
        title="🌧️ Précipitations annuelles"
    )
    fig_precip_annual.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Année",
        yaxis_title="Précipitations (mm)",
        font=dict(family="Poppins", color="#e8e8e8"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', dtick=1),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        legend=dict(title="Département", bgcolor='rgba(0,0,0,0.3)')
    )
    st.plotly_chart(fig_precip_annual, use_container_width=True)

# =====================
# FOOTER
# =====================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
    <div style="
        text-align: center;
        padding: 20px;
        background: rgba(255,255,255,0.03);
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.05);
    ">
        <p style="color: #666; margin: 0; font-size: 0.85rem;">
            🔄 Comparaison : <strong>Plotly</strong> | 
            💾 Données : <strong>Météo-France</strong> | 
            🎓 Master 2 GMS: Projet Géodata-Visualisation |
            👩‍💻 <strong style="color: #00d2ff;">Alia AL MOBARIK</strong>
        </p>
    </div>
""", unsafe_allow_html=True)
