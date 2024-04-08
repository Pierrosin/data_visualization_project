import pandas as pd
import geopandas as gpd

mapping = {
    'Ahuntsic - Cartierville': 'Ahuntsic-Cartierville',
    'Villeray-Saint-Michel - Parc-Extension': 'Villeray-Saint-Michel-Parc-Extension',
    'Rosemont - La Petite-Patrie': 'Rosemont-La Petite-Patrie',
    'Mercier - Hochelaga-Maisonneuve': 'Mercier-Hochelaga-Maisonneuve',
    'Le Plateau-Mont-Royal': 'Le Plateau-Mont-Royal',
    'Ville-Marie': 'Ville-Marie',
    'Côte-des-Neiges - Notre-Dame-de-Grâce': 'Côte-des-Neiges-Notre-Dame-de-Grâce',
    'Le Sud-Ouest': 'Le Sud-Ouest',
    'Rivière-des-Prairies - Pointe-aux-Trembles': 'Rivière-des-Prairies-Pointe-aux-Trembles',
    'Saint-Léonard': 'Saint-Léonard',
    'LaSalle': 'LaSalle',
    'Verdun': 'Verdun',
    'Pierrefonds - Roxboro': 'Pierrefonds-Roxboro',
    'Saint-Laurent': 'Saint-Laurent'
}


def preprocess_df(df) : 
    df['Date_plantation'] = pd.to_datetime(df['Date_plantation'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df["Date_releve"] = pd.to_datetime(df["Date_releve"], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    # Enlever les valeurs manquantes
    df = df.dropna(subset=['Date_plantation', 'Date_releve'])
    # Créer une colonne avec les dates en string
    df['Date_plantation_format'] = df['Date_plantation'].dt.strftime('%Y-%m-%d')
    df['Date_releve_format'] = df['Date_releve'].dt.strftime('%Y-%m-%d')
    # Remplacer les noms des arrondissements
    df['ARROND_NOM'] = df['ARROND_NOM'].map(mapping)
    # Enlever les espaces inutiles des rues
    df['Rue'] = df['Rue'].str.replace(r'\s{2,}', ' ', regex=True)

    return df

def removeOutliers(df):
    # clean = df[df['COTE'].isin(['N', 'S', 'E', 'O', 'I', 'P'])]
    clean = df
    clean = clean[(clean['Coord_X'] > 270000) & (clean['Coord_X'] < 310000) & (clean['Coord_Y'] > 5030000) & (clean['Coord_Y'] < 5070000)]
    clean = clean.dropna(subset=['SIGLE', 'Essence_latin', 'Essence_fr', 'ESSENCE_ANG'])
    clean = clean[clean['DHP'] < 300]
    clean = clean[(clean['Date_plantation'].dt.year > 1800) & (clean['Date_plantation'].dt.year < 2024) & (clean['Date_plantation'].dt.year <= clean['Date_releve'].dt.year)]
    # clean['Date_plantation'] = pd.to_datetime(clean['Date_plantation'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    clean = clean.dropna(subset=['Date_plantation'])
    clean = clean[(clean['Date_releve'].dt.year > 1950) & (clean['Date_releve'].dt.year < 2024)]
    # clean['Date_releve'] = pd.to_datetime(clean['Date_releve'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    clean = clean.dropna(subset=['Date_releve'])
    clean = clean[(clean['Longitude'] > -74) & (clean['Longitude'] < -73) & (clean['Latitude'] > 45) & (clean['Latitude'] < 46)]
    clean = clean.dropna(subset=['ARROND', 'ARROND_NOM'])
    clean = clean.dropna(subset=['Rue'])

    return clean

def getSpeciesList():
    df = pd.read_csv('assets/arbres-publics.csv')
    return list(pd.unique(df['Essence_fr']))


def get_neighborhoods(montreal_data):
    locations = []
    for feature in montreal_data.get('features', []):
        properties = feature.get('properties', {})
        nom = properties.get('NOM', None)
        if nom:
            locations.append(nom)

    return locations


def get_nb_trees_district(df, min_plant_date, max_plant_date, min_dhp, max_dhp, species=None):
    # Filtrer les arbres plantés entre les dates min et max
    filtered_df = df[(df['Date_plantation'] >= min_plant_date) & (df['Date_plantation'] <= max_plant_date)]

    # Filtrer les arbres avec DHP entre min et max
    filtered_df = filtered_df[(filtered_df['DHP'] >= min_dhp) & (filtered_df['DHP'] <= max_dhp)]

     # Filtrer les arbres pour inclure seulement les espèces spécifiées
    if species:
        filtered_df = filtered_df[filtered_df['Essence_fr'].isin(species)]

    # Compter le nombre d'arbres par arrondissement
    trees_per_district = filtered_df.groupby(['ARROND', 'ARROND_NOM']).size().reset_index(name='Nombre_Arbres')

    return trees_per_district


def get_missing_districts(tree_count_per_district, locations):
    # Liste des arrondissements présents dans le DataFrame
    existing_districts = tree_count_per_district['ARROND_NOM'].tolist()

    # Liste des arrondissements à ajouter
    districts_to_add = [district for district in locations if district not in existing_districts]

    # Créer un DataFrame pour les arrondissements manquants avec NaN pour le nombre d'arbres
    missing_districts_data = pd.DataFrame({'ARROND_NOM': districts_to_add, 'Nombre_Arbres': "Pas de données", 'AIRE': "Pas de données", 'Densite': "Pas de données"})
    
    return missing_districts_data


def add_density(df, geojson_path):
    data = gpd.read_file(geojson_path)

    # Sélectionner uniquement les colonnes 'NOM' et 'AREA'
    district_areas = data[['NOM', 'AIRE']]

    # Joindre les données des arrondissements avec les données d'aire
    district_data = pd.merge(df, district_areas, left_on='ARROND_NOM', right_on='NOM', how='left')

    # Supprimer la colonne 'NOM' redondante
    district_data.drop(columns=['NOM'], inplace=True)
    
    # Convertir l'aire en km² et calculer la densité d'arbres
    district_data['AIRE'] = district_data['AIRE'] / 1000000
    district_data['Densite'] = round(district_data['Nombre_Arbres'] / district_data['AIRE'])

    return district_data
