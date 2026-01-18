# 🌦️ Dashboard Météo PACA

Dashboard interactif d'analyse météorologique de la région PACA (2020-2023).

## 🚀 Démo en ligne

[Accéder au Dashboard](https://your-app-name.streamlit.app)

## 📊 Fonctionnalités

- **Carte Interactive** : Visualisation spatiale avec heatmaps température
- **Analyses Climatiques** : Évolution temporelle température, précipitations
- **Comparaison** : Analyse inter-départementale

## 🛠️ Installation locale

```bash
# Cloner le repo
git clone https://github.com/Aliaalmobarik/meteo-dashboard.git
cd meteo-dashboard

# Installer les dépendances
pip install -r requirements.txt

# Lancer le dashboard
streamlit run app.py
```

## 📁 Structure

```
meteo_dashboard/
├── app.py                 # Page d'accueil
├── pages/
│   ├── 1_Carte.py        # Carte interactive
│   ├── 2_Analyses.py     # Analyses temporelles
│   └── 3_Comparaison.py  # Comparaison départements
├── data/
│   ├── clean/            # Données météo
│   └── SHP_meteo.*       # Shapefiles PACA
└── requirements.txt
```

## 📈 Données

- **Source** : Météo-France
- **Période** : 2020-2023
- **Zone** : Région PACA (6 départements)
- **Variables** : Température, Précipitations, Humidité, Vent

## 👩‍💻 Auteur

**Alia AL MOBARIK** - M2 Géomatique

## 📄 Licence

MIT License
