import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
from pathlib import Path

# =====================
# CONFIGURATION PAGE
# =====================
st.set_page_config(
    page_title="🌍 GeoMétéo - Carte",
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
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif !important;
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
    }
    
    [data-testid="stMetricValue"] {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .main-title {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, rgba(0,210,255,0.1) 0%, rgba(58,123,213,0.1) 100%);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 30px;
    }
    
    .map-container {
        border-radius: 20px;
        overflow: hidden;
        border: 2px solid rgba(0,210,255,0.2);
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

@st.cache_data
def load_shp():
    shp_path = DATA_DIR / "SHP_meteo.shp"
    gdf = gpd.read_file(shp_path)
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs(epsg=4326)
    return gdf

df = load_data()
gdf_dept = load_shp()

noms_mois = {
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
            <p style="color: #888; font-size: 0.8rem;">Carte Interactive</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
        <p style="color: #00d2ff; font-size: 0.9rem; margin-bottom: 15px; padding-left: 5px;">📍 Navigation</p>
    """, unsafe_allow_html=True)
    
    st.page_link("app.py", label="🏠 Accueil")
    st.page_link("pages/1_Carte.py", label="🗺️ Carte")
    st.page_link("pages/2_Analyses.py", label="📈 Analyses")
    st.page_link("pages/3_Comparaison.py", label="🔄 Comparaison")
    
    st.markdown("---")
    
    st.markdown("### 📅 Filtres Temporels")
    
    years = sorted(df["date"].dt.year.unique())
    year = st.selectbox("Année", years, index=len(years)-1)
    
    months = list(range(1, 13))
    month = st.selectbox(
        "Mois", months, index=6,
        format_func=lambda x: noms_mois.get(x, str(x))
    )
    
    st.markdown("---")
    st.markdown("### 🗺️ Zone géographique")
    
    deps = sorted(df["dep"].dropna().unique())
    selected_dep = st.selectbox(
        "Département",
        ["Tous"] + list(deps),
        format_func=lambda x: "🌍 Tous les départements" if x == "Tous" else f"📍 Département {x}"
    )

# =====================
# FILTRAGE
# =====================
mask = (df["date"].dt.year == year) & (df["date"].dt.month == month)
if selected_dep != "Tous":
    mask &= df["dep"] == selected_dep
df_filtered = df[mask]

# =====================
# PAGE PRINCIPALE
# =====================
st.markdown("""
    <div class="main-title">
        <h1>🌍 Carte Météorologique PACA</h1>
        <p style="color: #a0a0a0;">Visualisation spatiale • Stations météo • Heatmaps</p>
    </div>
""", unsafe_allow_html=True)

# KPIs
st.markdown("### 📊 Statistiques")

k1, k2, k3, k4 = st.columns(4)

with k1:
    temp_moy = df_filtered["T"].mean() if "T" in df_filtered.columns else 0
    st.metric("🌡️ Température Moyenne", f"{temp_moy:.1f}°C")

with k2:
    precip_tot = df_filtered["RR1"].sum() if "RR1" in df_filtered.columns else 0
    st.metric("🌧️ Précipitations Totales", f"{precip_tot:.1f} mm")

with k3:
    hum_moy = df_filtered["U"].mean() if "U" in df_filtered.columns else 0
    st.metric("💧 Humidité Moyenne", f"{hum_moy:.0f}%")

with k4:
    nb_stations = df_filtered["NOM_USUEL"].nunique() if "NOM_USUEL" in df_filtered.columns else 0
    st.metric("📍 Stations", nb_stations)

st.markdown("<br>", unsafe_allow_html=True)

# =====================
# CARTE
# =====================
st.markdown("### 🗺️ Carte Interactive")

# Centre de la carte
center = [43.8, 6.0]
zoom = 7 if selected_dep == "Tous" else 9

m = folium.Map(
    location=center,
    zoom_start=zoom,
    tiles="CartoDB dark_matter",
    control_scale=True
)

# Couche GeoJSON
if gdf_dept is not None:
    folium.GeoJson(
        gdf_dept,
        name="Départements",
        style_function=lambda x: {
            "fillColor": "#00d2ff",
            "fillOpacity": 0.1,
            "color": "#00d2ff",
            "weight": 2,
        }
    ).add_to(m)

# Heatmap température
if len(df_filtered) > 0 and "lat" in df_filtered.columns and "lon" in df_filtered.columns:
    # Agrégation par station
    stations = df_filtered.groupby(["NOM_USUEL", "lat", "lon"]).agg({
        "T": "mean",
        "RR1": "sum"
    }).reset_index()
    
    # Heatmap
    if len(stations) > 0:
        heat_data = [[row["lat"], row["lon"], row["T"]] for _, row in stations.iterrows() if pd.notna(row["T"])]
        if heat_data:
            HeatMap(
                heat_data,
                radius=30,
                blur=20,
                gradient={0.2: "#00d2ff", 0.4: "#3a7bd5", 0.6: "#ff9900", 0.8: "#ff6b35", 1: "#cc0000"}
            ).add_to(m)
    
    # Marqueurs
    for _, row in stations.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8,
            popup=f"""
                <b>{row['NOM_USUEL']}</b><br>
                🌡️ T: {row['T']:.1f}°C<br>
                🌧️ Précip: {row['RR1']:.1f} mm
            """,
            color="#00d2ff",
            fill=True,
            fill_color="#00d2ff",
            fill_opacity=0.7
        ).add_to(m)

folium.LayerControl().add_to(m)

st.markdown('<div class="map-container">', unsafe_allow_html=True)
st_folium(m, width="100%", height=600)
st.markdown('</div>', unsafe_allow_html=True)

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
            📊 Données : <strong>Météo-France 2020-2023</strong> | 
            🗺️ <strong>Folium & Leaflet</strong> |
            👩‍💻 <strong style="color: #00d2ff;">Alia AL MOBARIK</strong>
        </p>
    </div>
""", unsafe_allow_html=True)
