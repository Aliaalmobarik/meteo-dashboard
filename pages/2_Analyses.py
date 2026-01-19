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
    page_title="Analyses Climatiques",
    page_icon="📈",
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
    
    .chart-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
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
    st.markdown("### 🗺️ Zone géographique")
    selected_dep = st.selectbox(
        "Département",
        ["Tous"] + sorted(df["DEPARTEMENT"].dropna().unique()),
        format_func=lambda x: "🌍 Tous" if x == "Tous" else f"📍 {x}"
    )

# =====================
# FILTRAGE
# =====================
df_filtered = df[df["annee"] == selected_year]
if month != "Tous":
    df_filtered = df_filtered[df_filtered["mois"] == month]
if selected_dep != "Tous":
    df_filtered = df_filtered[df_filtered["DEPARTEMENT"] == selected_dep]

# =====================
# TITRE
# =====================
st.markdown("""
    <div class="main-title">
        <h1>📈 Analyses Climatiques Avancées</h1>
        <p style="color: #a0a0a0;">Statistiques temporelles • Visualisations interactives</p>
    </div>
""", unsafe_allow_html=True)

# Contexte
mois_label = "Année complète" if month == "Tous" else noms_mois.get(month, month)
dep_label = "France entière" if selected_dep == "Tous" else f"Département {selected_dep}"
st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, rgba(0,210,255,0.15) 0%, rgba(58,123,213,0.15) 100%);
        border-radius: 15px;
        padding: 15px 25px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
        text-align: center;
    ">
        <span style="color: #e8e8e8;">📍 <strong style="color: #00d2ff;">{dep_label}</strong> | 
        📅 <strong style="color: #00d2ff;">{selected_year}</strong> | 
        🗓️ <strong style="color: #00d2ff;">{mois_label}</strong></span>
    </div>
""", unsafe_allow_html=True)

# =====================
# GRAPHIQUES - ÉVOLUTION ANNUELLE (toutes années)
# =====================
st.markdown("### 📅 Évolution Annuelle (toutes les années)")

# Filtrer par département seulement pour les graphiques annuels
df_annual = df.copy()
if selected_dep != "Tous":
    df_annual = df_annual[df_annual["DEPARTEMENT"] == selected_dep]

col_a1, col_a2 = st.columns(2)

# --- Température moyenne annuelle ---
with col_a1:
    temp_annual = df_annual.groupby("annee")["T"].mean().reset_index()
    
    fig_temp_annual = px.line(
        temp_annual, 
        x="annee", 
        y="T",
        markers=True,
        title="🌡️ Température moyenne par année"
    )
    fig_temp_annual.update_traces(
        line=dict(color="#ff6b6b", width=4),
        marker=dict(size=12, color="#ff6b6b", symbol="circle")
    )
    fig_temp_annual.add_trace(go.Scatter(
        x=temp_annual["annee"],
        y=temp_annual["T"],
        fill='tozeroy',
        fillcolor='rgba(255, 107, 107, 0.2)',
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=False
    ))
    fig_temp_annual.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Année",
        yaxis_title="Température (°C)",
        font=dict(family="Poppins", color="#e8e8e8"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', dtick=1),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig_temp_annual, use_container_width=True)

# --- Précipitations annuelles ---
with col_a2:
    precip_annual = df_annual.groupby(["annee", "NUM_POSTE"])["RR1"].sum().reset_index()
    precip_annual = precip_annual.groupby("annee")["RR1"].mean().reset_index()
    
    fig_precip_annual = px.bar(
        precip_annual,
        x="annee",
        y="RR1",
        title="🌧️ Précipitations moyennes par année"
    )
    fig_precip_annual.update_traces(marker_color='#4ecdc4')
    fig_precip_annual.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Année",
        yaxis_title="Précipitations (mm)",
        font=dict(family="Poppins", color="#e8e8e8"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', dtick=1),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig_precip_annual, use_container_width=True)

# =====================
# GRAPHIQUES - LIGNE 1 : Température & Précipitations MENSUELLES
# =====================
st.markdown("### 🌡️ Évolution Mensuelle / Journalière")

col1, col2 = st.columns(2)

# --- Température moyenne mensuelle ---
with col1:
    if month == "Tous":
        # Moyenne mensuelle
        temp_monthly = df_filtered.groupby("mois")["T"].mean().reset_index()
        temp_monthly["mois_nom"] = temp_monthly["mois"].map(noms_mois)
        
        fig_temp = px.line(
            temp_monthly, 
            x="mois_nom", 
            y="T",
            markers=True,
            title=f"🌡️ Température moyenne mensuelle ({selected_year})"
        )
        fig_temp.update_traces(
            line=dict(color="#ff6b6b", width=3),
            marker=dict(size=10, color="#ff6b6b")
        )
        # Ajouter aire sous la courbe
        fig_temp.add_trace(go.Scatter(
            x=temp_monthly["mois_nom"],
            y=temp_monthly["T"],
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.2)',
            line=dict(color='rgba(0,0,0,0)'),
            showlegend=False
        ))
    else:
        # Moyenne journalière pour le mois sélectionné
        df_filtered["jour"] = df_filtered["date"].dt.day
        temp_daily = df_filtered.groupby("jour")["T"].mean().reset_index()
        
        fig_temp = px.line(
            temp_daily, 
            x="jour", 
            y="T",
            markers=True,
            title=f"🌡️ Température moyenne journalière ({noms_mois[month]} {selected_year})"
        )
        fig_temp.update_traces(
            line=dict(color="#ff6b6b", width=3),
            marker=dict(size=8, color="#ff6b6b")
        )
    
    fig_temp.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="",
        yaxis_title="Température (°C)",
        font=dict(family="Poppins", color="#e8e8e8"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig_temp, use_container_width=True)

# --- Précipitations cumulées ---
with col2:
    if month == "Tous":
        # Cumul mensuel par station puis moyenne
        precip_monthly = df_filtered.groupby(["mois", "NUM_POSTE"])["RR1"].sum().reset_index()
        precip_monthly = precip_monthly.groupby("mois")["RR1"].mean().reset_index()
        precip_monthly["mois_nom"] = precip_monthly["mois"].map(noms_mois)
        
        fig_precip = px.bar(
            precip_monthly,
            x="mois_nom",
            y="RR1",
            title=f"🌧️ Précipitations moyennes mensuelles ({selected_year})"
        )
        fig_precip.update_traces(marker_color='#4ecdc4')
    else:
        df_filtered["jour"] = df_filtered["date"].dt.day
        precip_daily = df_filtered.groupby(["jour", "NUM_POSTE"])["RR1"].sum().reset_index()
        precip_daily = precip_daily.groupby("jour")["RR1"].mean().reset_index()
        
        fig_precip = px.bar(
            precip_daily,
            x="jour",
            y="RR1",
            title=f"🌧️ Précipitations journalières ({noms_mois[month]} {selected_year})"
        )
        fig_precip.update_traces(marker_color='#4ecdc4')
    
    fig_precip.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="",
        yaxis_title="Précipitations (mm)",
        font=dict(family="Poppins", color="#e8e8e8"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig_precip, use_container_width=True)

# =====================
# GRAPHIQUES - LIGNE 2 : Humidité & Rose des vents
# =====================
st.markdown("### 💧 Humidité & 🧭 Rose des Vents")

col3, col4 = st.columns(2)

# --- Humidité (Bar Chart) ---
with col3:
    if month == "Tous":
        humid_monthly = df_filtered.groupby("mois")["U"].mean().reset_index()
        humid_monthly["mois_nom"] = humid_monthly["mois"].map(noms_mois)
        
        fig_humid = px.bar(
            humid_monthly,
            x="mois_nom",
            y="U",
            title=f"💧 Humidité moyenne mensuelle ({selected_year})",
            color="U",
            color_continuous_scale=["#ffecd2", "#fcb69f", "#ff9a9e", "#a18cd1", "#5fc3e4"]
        )
    else:
        df_filtered["jour"] = df_filtered["date"].dt.day
        humid_daily = df_filtered.groupby("jour")["U"].mean().reset_index()
        
        fig_humid = px.bar(
            humid_daily,
            x="jour",
            y="U",
            title=f"💧 Humidité moyenne journalière ({noms_mois[month]} {selected_year})",
            color="U",
            color_continuous_scale=["#ffecd2", "#fcb69f", "#ff9a9e", "#a18cd1", "#5fc3e4"]
        )
    
    fig_humid.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="",
        yaxis_title="Humidité (%)",
        font=dict(family="Poppins", color="#e8e8e8"),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_humid, use_container_width=True)

# --- Rose des Vents ---
with col4:
    # Préparation des données pour la rose des vents
    wind_data = df_filtered[["DD", "FF"]].dropna()
    
    if len(wind_data) > 0:
        # Catégoriser les directions (DD est en degrés, 0-360)
        directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
                     "S", "SSO", "SO", "OSO", "O", "ONO", "NO", "NNO"]
        
        # Convertir les degrés en catégories (16 secteurs de 22.5° chacun)
        wind_data = wind_data.copy()
        
        # Fonction pour convertir degrés en direction
        def deg_to_direction(deg):
            if pd.isna(deg):
                return None
            # Ajuster pour que N soit centré sur 0°
            deg = (deg + 11.25) % 360
            idx = int(deg // 22.5)
            return directions[idx % 16]
        
        wind_data["direction_cat"] = wind_data["DD"].apply(deg_to_direction)
        
        # Catégoriser la vitesse du vent
        wind_data["vitesse_cat"] = pd.cut(
            wind_data["FF"],
            bins=[0, 2, 4, 6, 8, 100],
            labels=["0-2 m/s", "2-4 m/s", "4-6 m/s", "6-8 m/s", ">8 m/s"]
        )
        
        # Compter les occurrences
        wind_counts = wind_data.groupby(["direction_cat", "vitesse_cat"]).size().reset_index(name="count")
        wind_counts["direction_cat"] = pd.Categorical(wind_counts["direction_cat"], categories=directions, ordered=True)
        wind_counts = wind_counts.sort_values("direction_cat")
        
        # Créer la rose des vents
        fig_wind = px.bar_polar(
            wind_counts,
            r="count",
            theta="direction_cat",
            color="vitesse_cat",
            title="🧭 Rose des Vents",
            color_discrete_sequence=["#00d2ff", "#3a7bd5", "#667eea", "#764ba2", "#f093fb"]
        )
        
        fig_wind.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Poppins", color="#e8e8e8"),
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    linecolor='rgba(255,255,255,0.1)'
                ),
                angularaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    linecolor='rgba(255,255,255,0.1)'
                )
            ),
            legend=dict(
                title="Vitesse",
                bgcolor='rgba(0,0,0,0.3)',
                bordercolor='rgba(255,255,255,0.1)'
            )
        )
        st.plotly_chart(fig_wind, use_container_width=True)
    else:
        st.warning("⚠️ Pas de données de vent disponibles pour cette période")

# =====================
# STATISTIQUES RÉCAPITULATIVES
# =====================
st.markdown("### 📊 Statistiques Récapitulatives")

stat1, stat2, stat3, stat4 = st.columns(4)

with stat1:
    st.metric(
        "🌡️ T° Max",
        f"{df_filtered['T'].max():.1f} °C",
        delta=f"Min: {df_filtered['T'].min():.1f}°C"
    )

with stat2:
    precip_total = df_filtered.groupby("NUM_POSTE")["RR1"].sum().mean()
    st.metric(
        "🌧️ Cumul Précip.",
        f"{precip_total:.1f} mm",
        delta="Moyenne/station"
    )

with stat3:
    st.metric(
        "💧 Humidité Max",
        f"{df_filtered['U'].max():.0f} %",
        delta=f"Min: {df_filtered['U'].min():.0f}%"
    )

with stat4:
    st.metric(
        "💨 Vent Max",
        f"{df_filtered['FF'].max():.1f} m/s",
        delta=f"Moy: {df_filtered['FF'].mean():.1f} m/s"
    )

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
            📊 Visualisations : <strong>Plotly</strong> | 
            💾 Données : <strong>Météo-France</strong> | 
            🎓 Master 2 GMS: Projet Géodata-Visualisation
            👩‍💻 <strong style="color: #00d2ff;">Alia AL MOBARIK</strong>
        </p>
    </div>
""", unsafe_allow_html=True)
