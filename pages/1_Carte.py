import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium

# =====================
# CONFIGURATION PAGE & CSS
# =====================
st.set_page_config(
    page_title="🌍 GeoMétéo Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS moderne avec glassmorphism, gradients et animations
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Cacher le menu de navigation automatique de Streamlit */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Global */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f3460 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e8e8e8;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif !important;
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }
    
    /* Metric Cards - Glassmorphism */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 210, 255, 0.2);
        border-color: rgba(0, 210, 255, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        color: #a0a0a0 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Selectbox & Slider */
    .stSelectbox, .stSlider {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 5px;
    }
    
    /* Info box */
    .stAlert {
        background: rgba(0, 210, 255, 0.1) !important;
        border: 1px solid rgba(0, 210, 255, 0.3) !important;
        border-radius: 15px !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Custom title banner */
    .main-title {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, rgba(0,210,255,0.1) 0%, rgba(58,123,213,0.1) 100%);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 30px;
        animation: fadeIn 1s ease-out;
    }
    
    .main-title h1 {
        font-size: 2.8rem !important;
        margin: 0 !important;
    }
    
    .main-title p {
        color: #a0a0a0;
        font-size: 1.1rem;
        margin-top: 10px;
    }
    
    /* Stats banner */
    .stats-banner {
        background: linear-gradient(90deg, rgba(0,210,255,0.15) 0%, rgba(58,123,213,0.15) 100%);
        border-radius: 15px;
        padding: 15px 25px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
        display: flex;
        justify-content: center;
        gap: 30px;
    }
    
    .stats-banner span {
        color: #e8e8e8;
        font-size: 1rem;
    }
    
    .stats-banner strong {
        color: #00d2ff;
    }
    
    /* Map container */
    .map-container {
        border-radius: 20px;
        overflow: hidden;
        border: 2px solid rgba(0,210,255,0.2);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
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

@st.cache_data
def load_shp():
    gdf = gpd.read_file("data/SHP_meteo.shp")
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs(epsg=4326)
    return gdf

df = load_data()
gdf_dept = load_shp()

# Dictionnaire pour mapper les numéros aux noms de mois (global)
noms_mois = {
    1: "🌨️ Janvier", 2: "❄️ Février", 3: "🌱 Mars", 4: "🌷 Avril", 
    5: "🌸 Mai", 6: "☀️ Juin", 7: "🌞 Juillet", 8: "🏖️ Août", 
    9: "🍂 Septembre", 10: "🍁 Octobre", 11: "🌧️ Novembre", 12: "⛄ Décembre"
}

# =====================
# SIDEBAR (Filtres déportés pour libérer l'espace)
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
    selected_year = st.select_slider(
        "Année",
        options=sorted(df["annee"].unique().astype(int)),
        value=int(df["annee"].min())
    )

    month = st.selectbox(
        "Mois",
        options=["Tous"] + list(range(1, 13)),
        index=0,
        format_func=lambda x: "📆 Tous les mois" if x == "Tous" else noms_mois.get(x, str(x))
    )

    st.markdown("---")
    st.markdown("### 🗺️ Zone géographique")
    selected_dep = st.selectbox(
        "Département",
        ["Tous"] + sorted(df["DEPARTEMENT"].dropna().unique()),
        format_func=lambda x: "🌍 Tous les départements" if x == "Tous" else f"📍 {x}"
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
                ⚡ Mise à jour en temps réel
            </p>
        </div>
    """, unsafe_allow_html=True)

# =====================
# LOGIQUE DE FILTRAGE
# =====================
df_t = df[df["annee"] == selected_year]
if month != "Tous":
    df_t = df_t[df_t["mois"] == month]

df_map = df_t.copy()
gdf_map = gdf_dept.copy()

if selected_dep != "Tous":
    df_map = df_map[df_map["DEPARTEMENT"] == selected_dep]
    gdf_map = gdf_map[gdf_map["dep"] == selected_dep]

# =====================
# PAGE PRINCIPALE
# =====================

# Titre principal avec banner
st.markdown("""
    <div class="main-title">
        <h1>🌍 Observatoire Météo Spatio-temporel</h1>
        <p>Analyse climatique avancée • Données Météo-France • Projet M2 GMS</p>
    </div>
""", unsafe_allow_html=True)

# Bannière de contexte
mois_label = "Tous les mois" if month == "Tous" else noms_mois.get(month, month)
dep_label = "Toute la région Provence-Alpes-Côte d'Azur" if selected_dep == "Tous" else f"Département {selected_dep}"
st.markdown(f"""
    <div class="stats-banner">
        <span>📍 <strong>{dep_label}</strong></span>
        <span>📅 <strong>{selected_year}</strong></span>
        <span>🗓️ <strong>{mois_label}</strong></span>
        <span>📊 <strong>{len(df_map):,}</strong> observations</span>
    </div>
""", unsafe_allow_html=True)

# --- KPIs stylisés ---
st.markdown("### 📊 Indicateurs Climatiques")

k1, k2, k3, k4 = st.columns(4)

precip_par_station = df_map.groupby("NUM_POSTE")["RR1"].sum().mean()

with k1:
    st.metric("🌡️ Température", f"{df_map['T'].mean():.1f} °C", 
              delta=f"Min: {df_map['T'].min():.1f}°C")
with k2:
    st.metric("💧 Humidité", f"{df_map['U'].mean():.1f} %",
              delta=f"Max: {df_map['U'].max():.0f}%")
with k3:
    st.metric("🌧️ Précipitations", f"{precip_par_station:.1f} mm",
              delta="Cumul moyen/station")
with k4:
    st.metric("⏲️ Pression", f"{df_map['PMER'].mean():.1f} hPa",
              delta=f"±{df_map['PMER'].std():.1f}")

st.markdown("<br>", unsafe_allow_html=True)

# =====================
# PRÉ-CALCUL SIG
# =====================
heat_temp = df_map.groupby(["LAT", "LON"], as_index=False)["T"].mean().dropna()
heat_rain = df_map.groupby(["LAT", "LON"], as_index=False)["RR1"].sum().mean() # Corrigé pour le cumul
stations = df_map[["LAT", "LON", "NOM_USUEL"]].drop_duplicates()

# =====================
# CARTE INTERACTIVE
# =====================
st.markdown("### 🗺️ Visualisation Cartographique")

# Centrage automatique sur le département sélectionné si filtré
if selected_dep != "Tous" and not gdf_map.empty:
    center = [gdf_map.geometry.centroid.y.mean(), gdf_map.geometry.centroid.x.mean()]
    zoom = 8
else:
    center = [46.6, 1.9]
    zoom = 6

# Carte avec style sombre moderne
m = folium.Map(
    location=center, 
    zoom_start=zoom, 
    tiles="CartoDB dark_matter",
    control_scale=True
)

# --- Couche GeoJSON avec style néon ---
folium.GeoJson(
    gdf_map,
    name="🗺️ Départements",
    style_function=lambda x: {
        "fillColor": "#00d2ff",
        "fillOpacity": 0.08,
        "color": "#00d2ff",
        "weight": 2,
    },
    highlight_function=lambda x: {
        "fillColor": "#00d2ff",
        "fillOpacity": 0.3,
        "color": "#ffffff",
        "weight": 3,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["nom", "dep"], 
        aliases=["📍 Nom:", "🔢 Code:"],
        style="background-color: rgba(0,0,0,0.8); color: white; border-radius: 10px; padding: 10px;"
    )
).add_to(m)

# --- Stations avec style moderne ---
cluster = MarkerCluster(name="📍 Stations météo")
for _, row in stations.iterrows():
    folium.CircleMarker(
        location=[row["LAT"], row["LON"]],
        radius=6,
        popup=f"<b style='color:#00d2ff;'>{row['NOM_USUEL']}</b>",
        color="#00d2ff",
        fill=True,
        fill_color="#00d2ff",
        fill_opacity=0.7,
        weight=2
    ).add_to(cluster)
cluster.add_to(m)

# --- Heatmaps avec gradients personnalisés ---
h1 = folium.FeatureGroup(name="🔥 Température (Moyenne)", show=True)
HeatMap(
    heat_temp.values.tolist(), 
    radius=22, 
    blur=18,
    gradient={0.2: "#3a7bd5", 0.4: "#00d2ff", 0.6: "#ffd700", 0.8: "#ff6b35", 1: "#ff0000"}
).add_to(h1)
h1.add_to(m)

h2 = folium.FeatureGroup(name="🌧️ Précipitations (Cumul)", show=False)
heat_rain_data = df_map.groupby(["LAT", "LON"], as_index=False)["RR1"].sum().dropna()
HeatMap(
    heat_rain_data.values.tolist(), 
    radius=22, 
    blur=18,
    gradient={0.2: "#e0f7fa", 0.4: "#4dd0e1", 0.6: "#0097a7", 0.8: "#006064", 1: "#1a237e"}
).add_to(h2)
h2.add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

# Affichage de la carte dans un container stylé
st.markdown('<div class="map-container">', unsafe_allow_html=True)
st_folium(m, width="100%", height=650)
st.markdown('</div>', unsafe_allow_html=True)

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
            💾 Données : <strong>Météo-France</strong> | 
            🗺️ Cartographie : <strong>Folium & Leaflet</strong> | 
            🎓 Master 2 GMS: Projet Géodata-Visualisation
            👩‍💻 <strong style="color: #00d2ff;">Alia AL MOBARIK</strong>
        </p>
    </div>
""", unsafe_allow_html=True)

# =====================
# FOOTER
# =====================
st.markdown("---")
st.caption("🛠️ Projet M2 GMS | Source : Météo-France | Réalisé avec Streamlit & Folium")