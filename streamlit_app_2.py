import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

st.markdown("""
    <style>
    /* Réduire les marges gauche et droite */
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)



# Charger les données uniquement si elles ne sont pas encore présentes dans la session
if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv("5_LFB_fusion.csv")

# Accéder aux données depuis session_state
df = st.session_state.df

@st.cache_data
def analyser_df(df):
    analyse = pd.DataFrame({
        'Nb NaN': df.isna().sum(),
        '% NaN': df.isna().mean() * 100,
        'Nb valeurs uniques': df.nunique()
    })

    return analyse



st.sidebar.title("Sommaire")
st.sidebar.image("logo DST.png", width=100)
pages = ["Introduction","Définition des variables", "Exploration", "Enrichissement", "Datavisualisation","Choix des variables","Preprocessing", "Modélisation","Conclusion"]
page = st.sidebar.radio("Aller vers", pages)
st.sidebar.title("Auteurs")
st.sidebar.write("Léa Vauchel\n\n"
                  "Anne-Sixtine Lerebours\n\n"
                  "Alix Lavoipierre\n\n"
                   "Célia Taider")

# === Page - Introduction ===

if page == "Introduction":
   

    st.markdown("<h1 style='text-align: center;'>Temps de réponse des pompiers (LFB)</h1>", unsafe_allow_html=True)
    st.image("Lfb_logo.jpg", width=100)
    st.header("Introduction")
    st.markdown("""
                <div style='font-size:20px;'> 
                L’objectif de notre sujet est d’<strong>analyser et/ou estimer les temps de réponse</strong>  \
                de la brigade des pompiers de Londres, <strong>London Fire Brigade</strong>, \
                que l’on appellera par son acronyme :  <span style='font-size:20px;font-weight:bold;color:#FF6961 ;'>  <strong>LFB</strong></span>
        <br><br>
                Nous disposions de :<br> </div>""", unsafe_allow_html=True)
    st.markdown("""
                <div style='font-size:20px;'> 
        -3 jeux de données sur les mobilisations de la LFB, avec les informations concernant les camions de pompiers déployés, et<br>
       - 2 jeux de données répertoriant les incidents de la LFB.""", unsafe_allow_html=True)
                
               
    st.write("")
    st.write("")
    st.markdown("""
                <div style='font-size:20px;'> 
                Nous avons concaténé les différents DataFrames des incidents d’une part, de la mobilisation d’autre part. \
                Ces deux nouveaux datasets ont été fusionnés par la fonction <strong>MERGE</strong>.<br>
        Les données officielles de la LFB, disponibles sur le London Datastore, fournissent des détails sur chaque incident \
                depuis janvier 2009,\
                 incluant le type d'incident, la localisation et la date. Ces informations sont accessibles en formats CSV et XLS.
                """, unsafe_allow_html=True)
    st.write("")
    st.markdown("""
                <div style='font-size:20px;'>
                 Au cours de la période 2009-2024, les pompiers de Londres sont intervenus chaque année sur plus de <strong>100 000 incidents</strong>.<br>
                 Le projet se concentre sur les incidents survenus dans les limites du Grand Londres et sur la réponse apportée par les camions de pompiers de la London Fire Brigade.<br> \
        La London Fire Brigade (LFB) dispose de <u>103 casernes</u> de pompiers opérationnelles réparties sur les <u>33 arrondissements</u> de Londres et la Cité de Londres.<br>
        Cette structure a été établie après la fermeture de 10 casernes en 2014, dans le cadre du Fifth London Safety Plan, visant à rationaliser les ressources.""", unsafe_allow_html=True)
    st.write("")
    st.markdown("<span style='font-size:20px ;'>Le fichier final a pour dimensions : <u>2 488 987 lignes et 60 colonnes</u>.</span>", unsafe_allow_html=True)
    st.markdown("<span style='font-size:20px;'>Le critère choisi pour la modélisation est le plan défini pour 2024-2029 par la LFB :</span> "  "<span style='font-size:20px;font-weight:bold;color:#FF6961 ;'>atteindre un temps de réponse < ou = à 6 minutes.</span>", unsafe_allow_html=True)
    st.write("")
    col1,col2,col3 = st.columns([1,2,1])
    with col2 :
        st.write("<h5><u>Localisation des casernes</u>", unsafe_allow_html=True)
        st.image("Londres.png", width=700)

    
elif page == "Définition des variables":
    st.markdown("<h1 style='text-align: center;'>Définition des variables</h1>", unsafe_allow_html=True)
    st.image("Lfb_logo.jpg", width=100)
    Variables=['IncidentNumber', 'DateOfCall','CalYear', 'TimeOfCall', 'HourOfCall',  'IncidentGroup', 'StopCodeDescription',  'SpecialServiceType','PropertyCategory', 'PropertyType', 'AddressQualifier', 'Postcode_full',
                'Postcode_district',  'UPRN',  'USRN', 'IncGeo_BoroughCode',  'IncGeo_BoroughName', 'ProperCase',
                  'IncGeo_WardCode','IncGeo_WardName', 'IncGeo_WardNameNew',  'Easting_m', 'Northing_m',  'Easting_rounded', 
                  'Northing_rounded',  'Latitude',  'Longitude',  'FRS', 'IncidentStationGround', 'FirstPumpArriving_AttendanceTime', 
                  'FirstPumpArriving_DeployedFromStation',  'SecondPumpArriving_AttendanceTime', 'SecondPumpArriving_DeployedFromStation',  
                  'NumStationsWithPumpsAttending',  'NumPumpsAttending', 'PumpCount',  'PumpMinutesRounded',  'NationalCost', 'NumCalls',  
                  'ResourceMobilisationId',  'Resource_Code', 'PerformanceReporting',  'DateAndTimeMobilised', 'DateAndTimeMobile', 'DateAndTimeArrived',  
                  'TurnoutTimeSeconds', 'TravelTimeSeconds', 'AttendanceTimeSeconds', 'DateAndTimeLeft', 'DateAndTimeReturned', 'DeployedFromStation_Code', 'DeployedFromStation_Name', 
                  'DeployedFromLocation',  'PumpOrder', 'PlusCode_Code', 'PlusCode_Description', 'DelayCodeId',  'DelayCode_Description',  
                  'BoroughName',  'WardName']
    Description=["Numéro de l'incident", "Date de l'appel", "Année", "Temps de l'appel","Heure de l'appel","Catégorie d'incident",
                 "Sous-catégorie d'incident","Type de service spécial","Catégorie de propriété","Sous-catégorie de propriété",
                 "Qualité du renseignement donné de l'adrese de l'incident","Code Postal","Code du district","identifiant attribué à chaque unité d'adresse",
                 "Identifiant attribué à chaque voie","Code de l'arrondissement","Nom de l'arrondissement","nom de l'arrondissement en minuscules","Code du quartier","Nom du quartier","Nouveau nom de quartier","Coordonnées Est",
                 "Coordonnées Nord","Coordonnées arrondies Est","Coordonnées arrondies Nord","Latitude","Longitude","Brigade de pompiers","Caserne correspondant au lieu de l'incident",
                 "Délai d'arrivée de la première unité","Nom de la caserne d'origine","Délai d'arrivée de la seconde unité","Caserne de départ de la seconde unité",
                 "Nombre de casernes engagées pour un incident","nombre de camions déployés pour un incident","Nombre total de camions déployés toutes casernes confondues pour un incident",
                 "Nombre de minutes d'intervention cumulées","Coût théorique de l'intervention","Nombre d'appels au 999 pour un incident","Id de l'unité de mobilisation","code de l'unité de mobilisation",
                 "Perfomance","Date et heure où les pompiers sont mobilisés","Date et heure du départ depuis la caserne","Date et Heure d'arrivée sur les lieux de l'incident","Temps écoulé entre l'alerte et le départ du camion","Temps de trajet",
                 "Temps écoulé entre l'alerte et l'arrivée sur les lieux de l'incident","Date et heure où l'unité quitte le lieu de l'incident","Date et heure du retour à la caserne",
                 "Code identifiant de la caserne","Nom de la caserne","Type de déploiement","Ordre d'intervention du camion","Code de mobilisation","Type de mobilisation","Code retard","Type de retard","Nom de l'arrondissement","Nom du quartier"]
    df = pd.DataFrame({
    "Nom de la variable": Variables,
    "Description": Description
})
    def highlight_firstpump(row):
            styles = [''] * len(row)
            if row['Nom de la variable'] == 'FirstPumpArriving_AttendanceTime':
                return  ['background-color: lightgreen'] * len(row)
            else:
                return [''] * len(row)
    
    styled_df = df.style.apply(highlight_firstpump, axis=1)


     # Convertir en HTML avec CSS
    html = styled_df.to_html()
    st.markdown(html, unsafe_allow_html=True) 

    


# === Page - Exploration ===
elif page == "Exploration":
     st.markdown("<h1 style='text-align: center;'>Exploration du jeu de données</h1>", unsafe_allow_html=True)
     st.image("Lfb_logo.jpg", width=100)


     st.markdown("""
    <div style='font-size:16px;'> Nous avons réalisé une analyse exploratoire des données afin d’en comprendre le sens et les caractéristiques :
                 <ul>
              <li>typologie des variables (catégorielles ou quantitatives, continues ou discrètes),
              <li>identification des modalités et valeurs présentes,
               <li>analyse de leur distribution,
                <li>détection de valeurs manquantes, de doublons, de données aberrantes,
                <li>ainsi que d’éventuelles incohérences ou disparités de format.
                 <ul>
                 </div>
    """, unsafe_allow_html=True
)
     st.write("")
# Création d' onglets
     st.markdown("""
<style>
/* Cible tous les boutons des onglets */
button[role="tab"] {
    font-size: 20px !important;   /* Taille de la police */
    padding: 12px 30px !important; /* Padding pour plus d'espace */
    min-width: 150px !important;  /* Largeur minimum */
}
</style>
""", unsafe_allow_html=True)
     
     tab1, tab2, tab3,tab4 = st.tabs(["Données manquantes", "Occurences","Outliers","Doublons"])

# Contenu du premier onglet
     
     with tab1:
        st.markdown("### Données manquantes")
        data = {"Column":["SpecialServiceType", "Postcode_full", "UPRN", "USRN", "IncGeo_WardCode","IncGeo_WardName","IncGeo_WardNameNew","Easting_m","Northing_m","Latitude","Longitude",
                                                                        "IncidentStationGround","FirstPumpArriving_AttendanceTime","FirstPumpArriving_DeployedFromStation","SecondPumpArriving_AttendanceTime","SecondPumpArriving_DeployedFromStation",
                                                                        "NumCalls","DateAndTimeMobile","TurnoutTimeSeconds","TravelTimeSeconds","DateAndTimeLeft",
                                                                        "DateAndTimeReturned","DeployedFromStation_Code","DeployedFromStation_Name",
                                                                        "DeployedFromLocation","DelayCodeId","DelayCode_Description","BoroughName","WardName"],     
         "%NaN":["77.71", "53.91", "7.91", "9.33","0.03","0.03","0.03","53.91","53.91","53.91","53.91","0.00009","0.0001","0.0007","41.19","41.19","0.07","1.23","1.24","1.24","2.27","52.21","0.00005","0.00005","0.04","74.65","74.65","65.12","65.1"]}
        df_nan = pd.DataFrame(data)

     # Fonction pour colorer la ligne souhaitée
        def highlight_firstpump(row):
            if row['Column'] == 'FirstPumpArriving_AttendanceTime':
                return ['background-color: lightgreen'] * len(row)
            else:
                return [''] * len(row)

      # Appliquer le style
        styled_df = df_nan.style.apply(highlight_firstpump, axis=1)

     # Convertir en HTML avec CSS
        html = styled_df.set_table_attributes('class="custom-table"').hide(axis="index").to_html()

      # Style CSS
        st.markdown("""
<style>
.custom-table {
    font-size: 15px;
    border-collapse: collapse;
    margin: 0 auto;
    width: auto;
}
.custom-table th {
    background-color: #f0f0f0;
    color: black;
    padding: 7px;
    text-align: center;
}
.custom-table td {
    padding: 7px;
    text-align: center;
    border: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

     # Afficher le tableau stylisé
        st.markdown(html, unsafe_allow_html=True)

        st.markdown("Il y a beaucoup de valeurs manquantes. Nous n'allons pas supprimer ces lignes pour éviter une perte d'information. Nous allons les remplacer. Cependant, nous nous en occuperons une fois que le jeu de données sera séparé en jeu d'entraînement et jeu de test : nous ne devons pas apporter d'information du jeu de test dans le jeu d'entraînement ce qui conduirait à un biais dans le Machine Learning.")
# Contenu du deuxième onglet
     with tab2:
        st.write("")
        st.markdown("""
<style>
/* Cible le selectbox et augmente la taille de police */
div[data-baseweb="select"] > div {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)
        
        colonnes_cat = ['IncidentGroup', 'StopCodeDescription', 'SpecialServiceType','PropertyCategory','DeployedFromLocation','DelayCode_Description']

        st.markdown("### Distribution des occurences")
        st.write("")
        variable = st.selectbox("### Sélectionner une variable catégorielle", colonnes_cat)

        @st.cache_data
        def calcul_distribution(df, col):
           dist = df[col].value_counts(normalize=True).reset_index()
           dist.columns = [col, '%']
           dist['%'] = (dist['%'] * 100).round(2)
           return dist

        def afficher_tableau_stylé(df):
            styled_df = df.style \
        .hide(axis="index") \
        .format({"%": "{:.2f}"}) \
        .set_table_styles([
            {'selector': 'th', 'props': [('font-size', '20px'), ('font-weight', 'bold')]},
            {'selector': 'td', 'props': [('font-size', '18px')]}
        ])

            html = styled_df.to_html()
            st.markdown(html, unsafe_allow_html=True)

# Dans ton app Streamlit :
        if variable:
           dist_df = calcul_distribution(df, variable)
           afficher_tableau_stylé(dist_df)

           st.write("")
# Contenu du troisième onglet : outliers
     with tab3:
        st.write("")
        st.markdown("### Outliers")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        data = [[311, 1, 229, 291, 369, 1200, 130]] 
        columns =["FirstPumpAttendanceTime"] 
        index = ["mean", "min","25%", "50%", "75%", "max","std"]
        df = pd.DataFrame(data, columns, index)
        
        table_html = df.to_html(classes='custom-table', border=0)

        st.markdown("""<style>.custom-table {
             width: 80%;  margin-left: auto; margin-right: auto; font-size: 14px;
        border-collapse: collapse;
    }.custom-table th, .custom-table td {
        padding: 8px 12px;
        border: 1px solid #ccc;
        text-align: center;
    }</style>
""", unsafe_allow_html=True)
        st.markdown(table_html, unsafe_allow_html=True)

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("Ces statistiques nous permettent d'apporter 2 arguments :\n\n"
                  "- Il existe des outliers (valeurs extrêmes ou aberrantes)\n\n"
                 "- Un écart-type (std) élevé : les données sont donc très dispersées ; avec l'impact des valeurs extrêmes.\n\n"
                 "Dans un deuxième temps, la datavisualisation nous permettra de confirmer les outliers")
        
# Contenu du quatrième onglet : doublons
     with tab4:
        st.markdown("### Doublons")
        st.write("")
        st.write("")
        st.write('Avec l\'utilisation de la méthode **drop** : **df.drop_duplicates** :')
        st.write("")
        st.markdown("""
                    <ul>
    <span style="color: #FF6961;">3 864 doublons ont été supprimés</span>
</ul>
""", unsafe_allow_html=True)
     
     

# === Page - Enrichissement:
elif page == "Enrichissement" : 
    st.markdown("<h1 style='text-align: center;'>Enrichissement des données</h1>", unsafe_allow_html=True)
    st.image("Lfb_logo.jpg", width=100)
    col1, col2, col3 = st.columns(3)
    with col1 :
        st.write("Pour faciliter la pertinence de la datavisualisation, nous avons segmenté la date complète avec de nouvelles variables.\n\n"
         "🕒   Ajout de variables temporelles :\n\n"
                 "- **Weekday**\n\n"
                 "- **Month**\n\n")
       

    with col2 :   
         st.write("")
         st.write("")
         st.write("")
         st.write("")
         st.write("")
         st.write("")
        
         st.write("")
         st.write("Nous avons récupéré des données météorologiques pour la période qui nous concerne (2009-2024) depuis une source de données mise en accès libre (fichiers excel de l'historique jour par jour de la météo sur Londres).\n\n"
                 "☀️  Nouvelles variables météorologiques :\n\n"
                 "- **Meteo**\n\n"
                 "- **Visibility**\n\n")
        
    with col3:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("📍 Dernier ajout : une variable géographique qui permet d'identifier si l'arrondissement est du centre de Londres ou en périphérie\n\n"
                 "- **Inner_outer**")
        st.write("")
        st.image("Inner_Outer copie.png", width=400)

elif page == "Datavisualisation" : 
    st.markdown("<h1 style='text-align: center;'>Datavisualisation</h1>", unsafe_allow_html=True)
    st.image("Lfb_logo.jpg", width=100)

    tab1, tab2, tab3 = st.tabs(["📊 Dataviz Univariée", "📈 Dataviz Multivariée", "🔥 Heatmap"])
   # Onglet 1 : Dataviz univariée  
    with tab1:
        st.write("")
        option = st.selectbox("Sélectionnez une variable",
    ("Distribution de la variable cible", 
    "Fréquence des incidents", 
    "Evolution des incidents", 
    "Répartition des fréquences d'incident selon Londres inner/outer",
    "Retard"))
        st.write("")
        
        if option == "Distribution de la variable cible":
             st.write("")
             st.image("Temps de réponse.png", width = 1200)
             st.write("")
             st.write("On constate beaucoup d'outliers qui peuvent biaiser ou invalider nos résultats de prédiction.\n")
             st.write("On a utilisé le méthode de **l'écart interquantile (IQR)** pour détecter et supprimer les temps de réponse supérieurs à **780s**.")
          
        elif option == "Fréquence des incidents":
             col1, col2= st.columns([1,1])
             with col1 :
                  st.image("Catégories d'incident.png", width=600)
             st.write("")
             with col2 :
                  st.write("")
                  st.write("")
                  st.write("")
                  st.write("")
                  st.write("")
                  st.write("")
                  st.write("")
                  st.write("")
                  st.write("")
                  st.write("")
                  st.write("Les fausses alarmes peuvent causer une perte relative de temps par rapport aux besoins réels")
        
        elif option == "Evolution des incidents":
             st.image("Evolution_incidents.png")
             st.markdown("On observe une diminution respective du nombre d'incidents en 2020 ; on peut l'associer au **confinement lors de la pandémie COVID-19**.")

        elif option == "Répartition des fréquences d'incident selon Londres inner/outer":
             st.image("Incidents Inner vs Outer.png", width=800)
             st.write("")
             st.write("")
             
        elif option == "Retard":
             st.image("Retard.png", width =800)
             st.markdown("<h5 style='font-size: 20px;'>On constate que dans 90% des cas il n'y a pas de retard</h5>", unsafe_allow_html=True)

           
    # 📈 Onglet 2 : Dataviz multivariée
    with tab2:
        st.write("")
        st.write("")
        

        st.markdown("### Temps de préparation selon le type d'incident")
        st.write("")
        st.image("temps de préparation.png", width= 900)

        st.write("")
            
        st.markdown("### Mois")
        st.image("Temps de réponse selon mois.png", width=600)
        st.write("")
        st.write("")

        st.markdown("### Heure")
        st.image("Temps de trajet selon heure.png", width=900)
        st.write("Les heures de journée rallongent le temps d'arrivée par rapport à la nuit")
        
        st.markdown("### Année")
        st.image("Evolution_temps_trajet.png", width=600)
    
        st.write("Le temps de trajet augmente année après année avec une augmentation notable entre 2009 et 2010")
        st.write("")
            
        st.write("")


        st.markdown("### Variable cible selon le lieu de l'incident")
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
                st.image("Réponse selon arrondissement.png", width=500)
        with col2 :
                st.image("Hilington.png", width = 300)
                st.image("Islington.png", width=300)
        


    
    # 🔥 Onglet 3 : Heatmap
    with tab3:
        st.write("")
        st.write("Carte thermique des corrélations entre variables.")
        st.image("Heatmap.png", width=1000)

# === Page - Choix des variables ===

elif page == "Choix des variables":
    st.markdown("<h1 style='text-align: center;'>Choix des variables</h1>", unsafe_allow_html=True)
    st.image("Lfb_logo.jpg", width=100)
    st.write("")
    st.write("")
    st.write("")
    st.markdown("<u><strong>VARIABLE CIBLE ou TARGET</strong></u>", unsafe_allow_html=True)
    st.markdown('<span style="font-size : 18px ;color: #FF6961 ;">FirstPumpArriving_AttendanceTime </span> = temps de réaction de la première unité', unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.markdown("<u><strong>VARIABLES EXPLICATIVES OU FEATURES</strong></u>", unsafe_allow_html=True)
    
   
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
        "Les variables numériques :\n\n")
        st.markdown("""
                    <li><span style="font-size : 18px ;color: #FF6961 ;">CalYear</span> = Année</li>
                    <li><span style="font-size : 18px ;color: #FF6961 ;">HourOfCall</span> = Heure</li> 
                    <li><span style="font-size : 18px ;color: #FF6961 ;">Easting_rounded</span> = Localisation est</li> 
                    <li><span style="font-size : 18px ;color: #FF6961 ;">Northing_rounded</span> = Localisation nord</li>""", unsafe_allow_html=True)
            
    with col2:
        st.markdown(
        "Les variables catégorielles :\n\n")
        
        st.markdown("""<ul>     
                          <li><span style="font-size : 18px ;color: #FF6961 ;">StopCodeDescription</span> = Type d'incident</li>
                     <li><span style="font-size : 18px ;color: #FF6961 ;">PropertyCategory</span> = Catégorie de propriété</li>  
                         <li><span style="font-size : 18px ;color: #FF6961 ;">DeployedFromStation_name</span> = Nom de la caserne </li>
                     <li><span style="font-size : 18px ;color: #FF6961 ;">Meteo</span> = Météo</li>
                                        <li><span style="font-size : 18px ;color: #FF6961 ;">Visibility</span> = Visibilité sur la route</li>""", unsafe_allow_html=True)
            

# === Page - Preprocessing ===
elif page == "Preprocessing":
    st.markdown("<h1 style='text-align: center;'>Preprocessing</h1>", unsafe_allow_html=True)
    st.image("Lfb_logo.jpg", width=100)
    st.markdown("""
<style>
/* Cible tous les boutons des onglets */
button[role="tab"] {
    font-size: 24px !important;   /* Taille de la police */
    padding: 12px 30px !important; /* Padding pour plus d'espace */
    min-width: 150px !important;  /* Largeur minimum */
}
</style>
""", unsafe_allow_html=True)
    tabs = st.tabs(["✂️ Split", "❓Gestion des NaN","🔢 Frequency Encoding", "🕹️ OneHotEncoder", "🔼 Ordinal Encoding", "⚖️ Standardisation"])

# Contenu du premier onglet
    with tabs[0]:
        st.write("")



      
        




        st.write("")
        st.markdown("""
    <div style='font-size:16px;'>Le <b>split</b> consiste à séparer le jeu de données en jeu test et en jeu d'entraînement : nous avons pris arbitrairement les proportions respectives de :<br><br>
                 <b>20% et 80%</b> et un <b>random_state</b> commun (valeur choisie : 42) entre les membres de l'équipe pour obtenir les mêmes résultats<br><br>
                 Le jeu d'entrainement sert à entraîner le modèle de Machine Learning, c'est-à-dire à trouver les paramètres du modèle qui séparent au mieux les classes.<br><br>
                 Le jeu de test sert à évaluer le modèle sur des données qu'il n'a jamais vues. Cette étape nous permettra d'évaluer la capacité du modèle à se généraliser.<br><br>
                 </div>
    """, unsafe_allow_html=True)
        st.markdown('<span style="color: #FF6961;">X_train, X_test, y_train, y_test = train_test_split(features, target, test_size = 0.2,random_state = 42)</span>', unsafe_allow_html=True)
        st.write("")
        st.write("")
       # Contenu du 2° onglet    
    with tabs[1]:
        st.write("")
        st.write("")
        st.write("La gestion des NaN a été faite après le split pour éviter toute fuite de données\n\n"
                 "Les variables avec un taux de NaN à 0.5%, telle **DeployedFromStation_Name**, on a choisi de supprimer les lignes concernées soit 8 lignes.\n\n"
                 "Tandis que les NaN des autres variables (**Meteo**, **Visibility**) ont été remplacées par leur mode grâce à **SimpleImputer**.\n\n"
                 "Cette étape est nécessaire après le split pour éviter la fuite des données et pour permettre de lancer le machine learning qui ne peut pas traiter des valeurs nulles")
        st.write("L'étape suivante est l'encodage :\n\n"
        "Son but est de transformer les données catégorielles en données chiffrées puisque les algorithmes de machine learning ne traitent que les données numériques")
        st.write("")
        st.write("Afin d'optimiser cette étape, nous avons choisi un encodage pertinent selon le nombre d'occurences par variables\n\n")

# Contenu du 3° onglet  
    with tabs[2]:
         st.write("")
         st.write("")
         st.write("Les variables avec plusieurs centaines de valeurs uniques ont été encodées par le frequency encoding pour éviter la multiplication des colonnes.\n\n"
                 "C'est le cas pour **DeployedFromStation_Name**, **Easting_rounded**, **Northing_rounded**.\n\n"
                 "Les variables **Easting_rounded** et **Norting_rounded** étant des variables numériques qualitatives (et non algébriques), elles ont été traitées comme des variables catégorielles.\n\n"
                 "Ce type d'encodage garde l'importance relative des valeurs les plus représentées.")
# Contenu du 4° onglet   
    with tabs[3]:
         st.write("")
         st.write("")
         st.write("Le OneHotEncoder consiste en une combinaison de codes binaires, créant autant de colonnes qu'il y a de valeurs uniques.\n\n"
                  "On estime l'encodage sur le jeu d'entraînement et on l'applique sur le jeu d'entraînement et de test."
                 "Cet encodage était adapté pour les variables avec des occurences comprises\n\n"
                 "entre 10 et 16 valeurs : **StopCodeDescription**, **PropertyCategory**.")
# Contenu du 5° onglet
    with tabs[4]:
         st.write("")
         st.write("")
         st.write("En dernier lieu, les dernières variables choisies ont des occurences avec un ordre d'importance.\n\n"
                 "Avec le Ordinal Encoding, la notion d'ordre a été conservée pour les variables : **Meteo** et **Visibility**.")
         
         st.markdown("Les valeurs restantes - l'heure et l'année - peuvent être potentiellement encodées par une transformation cyclique (opération qu'on ne maîtrisait pas).\n\n"
                     "En revanche, nous avons appliqué la standardisation comme expliqué ci-après.")
# Contenu du 6° onglet    
    with tabs[5]:
         st.write("")
         st.write("")
         st.write("Les modèles de machine learning sont sensibles aux différences d'échelle d'où le choix d'une standardisation qui a évité tout biais possible.\n\n"
                 "La fonction de scikit learn choisie est **StandardScaler**.")
        

# === Page - Modélisation ===
elif page == "Modélisation":
    st.markdown("<h1 style='text-align: center;'>Modélisation</h1>", unsafe_allow_html=True)
    st.image("Lfb_logo.jpg", width=100)
    st.write("La variable cible étant une variable continue, nous avons choisi, dans un premier temps d'entraîner des méthodes de régression."
             "Pour évaluer et comparer la puissance de prédiction de ces premiers modèles, nous avons choisi les métriques suivantes:\n\n")

# Graphique de régression (affichage de la relation entre la cible et une feature)
    with st.expander("**MODELES DE REGRESSION**"):
        choix = st.radio("Sélectionnez un modèle",["Linear Regression", "Decision Tree Regressor", "Random Forest Regressor", "SGD Regressor", "KNN Regressor","Tableau comparatif"])  
        
        if choix == "Linear Regression":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>LINEAR REGRESSION</b></h4>
            <p><b>Mean Absolute Error = 89.72</b></p>
            <p><b>Mean Squared Error = 14049.17</b></p>
            <p><b>Root Mean Squared Error = 118.53</b></p>
            <p><b>R² Score = 118.53</b></p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Decision Tree Regressor":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>DECISION TREE REGRESSOR</b></h4>
            <p><b>Mean Absolute Error = 207.25</b></p>
            <p><b>Mean Squared Error = 63919.10</b></p>
            <p><b>Root Mean Squared Error = 252.82</b></p>
            <p><b>R² Score = -3.32</b></p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Random Forest Regressor":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>RANDOM FOREST REGRESSOR</b></h4>
            <p><b>Mean Absolute Error = 88.15</b></p>
            <p><b>Mean Squared Error = 13649.74	</b></p>
            <p><b>Root Mean Squared Error = 116.83</b></p>
            <p><b>R² Score = 0.08</b></p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "SGD Regressor":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>SGD REGRESSOR</b></h4>
            <p><b>Mean Absolute Error = 2.20e14	</b></p>
            <p><b>Mean Squared Error = 4.92e30</b></p>
            <p><b>Root Mean Squared Error = 2.22e15</b></p>
            <p><b>R² Score = 3.32e26</b></p>
        </div>
    """, unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            image = Image.open("SGD_REGRESSOR.png")
            col1, col2, col3 = st.columns([1, 1.5, 1])
            with col2:
                st.image(image, width=500)
            
            
        if choix == "KNN Regressor":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>KNN REGRESSOR</b></h4>
            <p><b>Mean Absolute Error = 94.11</b></p>
            <p><b>Mean Squared Error = 15144</b></p>
            <p><b>Root Mean Squared Error = 123.06</b></p>
            <p><b>R² Score = -0.02</b></p>
        </div>
    """, unsafe_allow_html=True)

        if choix == "Tableau comparatif":
            data = [[89.72, "14049.17", 118.53, 0.05], [207.25, "63919.10", 252.82, -3.32], [88.15, "13649.74", 116.83, 0.08],["2.20e14", "4.92e30", "2.22e15", "3.32e26"],[94.11, "15144", 123.06, -0.02]]  
            df = pd.DataFrame(data, columns = ["MAE", "MSE", "RMSE", "R2"], index =["Linear Regression", "Decision Tree Regressor", "Random Forest Regressor", "SGD Regressor", "KNN Regressor"])
        
            table_html = df.to_html(classes='custom-table', border=0)

            st.markdown("""<style>.custom-table {
             width: 80%;  margin-left: auto; margin-right: auto; font-size: 14px;
        border-collapse: collapse;
    }.custom-table th, .custom-table td {
        padding: 8px 12px;
        border: 1px solid #ccc;
        text-align: center;
    }</style>
""", unsafe_allow_html=True)
            st.markdown(table_html, unsafe_allow_html=True)

        

        
# Classification binaire
        
    with st.expander("**MODELES DE CLASSIFICATION BINAIRE**"):
        st.write("Nous ne sommes pas parvenues à obtenir un modèle de régression performant malgré les tentatives d'optimisation.\n\n"
             "Nous avons donc adopté en deuxième étape des modèles de classification binaire.\n\n"
             "Les classes choisies pour la variable cible sont bornées par la valeur de 6 minutes, qui est le critère choisi pour le plan de la LFB\n\n")
        st.markdown("""
                    <div style="text-align: center;">
    <h5><u><strong>Répartition des classes</strong></u></h5>
</div>
<div style="text-align: center; color:#FF6961">
    <p><b>Classe 0</b> : > 6 minutes </p>
    <p><b>Classe 1</b> : < = 6 minutes (objectif)</p>
    </div>
""", unsafe_allow_html=True)
                  
        choix = st.radio("Sélectionnez un modèle",["Logistic Regression", "Decision Tree Classifier", "Random Forest Classifier", "XGB Classifier", "KNN Classifier","Linear SVC","Tableau comparatif et importance des variables"])  
    
        if choix == "Logistic Regression":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>LOGISTIC REGRESSION</b></h4>
            <p><b>Accuracy = 0.71</b></p>
            <p><b>Precision classe 0 = 0.54</b></p>
            <p><b>Precision classe 1 = 0.71</b></p>
            <p><b>Recall classe 0 = 0.00</b></p>
            <p><b>Recall classe 1 = 1.00</b></p>
                        <p><b>F1-score classe 0 = 0.00</b></p>
            <p><b>F1-score classe 1 = 0.83</b></p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Decision Tree Classifier":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>DECISION TREE CLASSIFIER</b></h4>
            <p><b>Accuracy= 0.70</b></p>
            <p><b>Precision classe 0 = 0.49</b></p>
            <p><b>Precision classe 1 = 0.79	</b></p>
            <p><b>Recall classe 0 = 0.49</b></p>
            <p><b>Recall classe 1 = 0.79</b></p>
                        <p><b>F1-score classe 0 = 0.49</b></p>
            <p><b>F1-score classe 1 = 0.79</b></p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Random Forest Classifier":
           st.markdown("""
        <div style="text-align: center;">
            <h4><b>RANDOM FOREST CLASSIFIER</b></h4>
            <p><b>Accuracy= 0.74</b></p>
            <p><b>Precision classe 0 = 0.61	</b></p>
            <p><b>Precision classe 1 = 0.77	</b></p>
            <p><b>Recall classe 0 = 0.31</b></p>
            <p><b>Recall classe 1 = 0.92</b></p>
                        <p><b>F1-score classe 0 = 0.41</b></p>
            <p><b>F1-score classe 1 = 0.84</b></p>
        </div>
    """, unsafe_allow_html=True)
            
            
        if choix == "XGB Classifier":
            st.markdown("""
       <div style="text-align: center;">
            <h4><b>XGB CLASSIFIER</b></h4>
            <p><b>Accuracy= 0.73</b></p>
            <p><b>Precision classe 0 = 0.68	</b></p>
            <p><b>Precision classe 1 = 0.74	</b></p>
            <p><b>Recall classe 0 = 0.15</b></p>
            <p><b>Recall classe 1 = 0.97</b></p>
                        <p><b>F1-score classe 0 = 0.24	</b></p>
            <p><b>F1-score classe 1 = 0.84</b></p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "KNN Classifier":
            st.markdown("""
       <div style="text-align: center;">
            <h4><b>KNN CLASSIFIER</b></h4>
            <p><b>Accuracy= 0.69</b></p>
            <p><b>Precision classe 0 = 0.37	</b></p>
            <p><b>Precision classe 1 = 0.72	</b></p>
            <p><b>Recall classe 0 = 0.09</b></p>
            <p><b>Recall classe 1 = 0.93</b></p>
                        <p><b>F1-score classe 0 = 0.15		</b></p>
            <p><b>F1-score classe 1 = 0.81</b></p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Linear SVC":
            st.markdown("""
       <div style="text-align: center;">
            <h4><b>LINEAR SVC</b></h4>
            <p><b>Accuracy= 0.71</b></p>
            <p><b>Precision classe 0 = 0.59	</b></p>
            <p><b>Precision classe 1 = 0.71	</b></p>
            <p><b>Recall classe 0 = 0.00</b></p>
            <p><b>Recall classe 1 = 1.00</b></p>
                        <p><b>F1-score classe 0 = 0.01</b></p>
            <p><b>F1-score classe 1 = 0.83</b></p>
        </div>
    """, unsafe_allow_html=True)

        if choix == "Tableau comparatif et importance des variables":
            st.write("")
            st.write("")
            data = [
        [0.71, 0.54, 0.71, 0.00, 1.00, 0.00, 0.83],
        [0.70, 0.49, 0.79, 0.49, 0.79, 0.49, 0.79],
        [0.74, 0.61, 0.77, 0.31, 0.92, 0.41, 0.84],
        [0.73, 0.68, 0.74, 0.15, 0.97, 0.24, 0.84],
        [0.69, 0.37, 0.72, 0.09, 0.93, 0.15, 0.81],
        [0.71, 0.59, 0.71, 0.00, 1.00, 0.01, 0.83]]
            df2 = pd.DataFrame(data,columns=[
            "Accuracy",
            "Precision Classe 0", "Precision Classe 1",
            "Recall Classe 0", "Recall Classe 1",
            "F1 Score Classe 0", "F1 Score Classe 1"],index=[
            "Logistic Regression", "Decision Tree Classifier",
            "Random Forest Classifier", "XGB Classifier",
            "KNN Classifier", "Linear SVC"])
         
            st.markdown(f"""
<div class="scrollable-table-container">
{df2.to_html(classes='custom-table', index=True)}
</div>
""", unsafe_allow_html=True)
    
            
# Classification multi-classes
    with st.expander("## **MODELES DE CLASSIFICATION MULTI-CLASSES**"):
        st.write("Nous avons fait le choix de découper notre variable cible en fonction de ses quartiles. Le but étant d’obtenir des échantillons de taille similaire et  ainsi permettre à notre modèle d’être plus performant. Dans un souci de compréhension, nous avons " \
            "arrondi ces quartiles à la minute la plus proche.")
        
        st.markdown("""
                    <div style="text-align: center;">
    <h5><u><strong>Répartition des classes</strong></u></h4>
</div>
<div style="text-align: center; color:#FF6961">
    <p><b>Classe 0</b> : ≤ à 4 minutes (28.66%)</p>
    <p><b>Classe 1</b> : entre 4 et 5 minutes (23.20%)</p>
    <p><b>Classe 2</b> : entre 5 et 6 minutes 30 secondes (6.43%)</p>
    <p><b>Classe 3</b> : entre 6 minutes 30 secondes et 13 minutes (21.71%)</p>
</div>
""", unsafe_allow_html=True)
            
        choix = st.radio("Sélectionnez un modèle",["Logistic Regression multi-classes", "Decision Tree Classifier multi-classes", "Random Forest Classifier multi-classes", "XGB Classifier multi-classes", "KNN Classifier multi-classes","Tableau comparatif et importance des variables multi-classes"])  
    
        st.write("")
        st.write("")
        st.write("")
        if choix == "Logistic Regression multi-classes":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>Logistic Regression</b></h4>""", unsafe_allow_html=True)
            col1,col2,col3, col4= st.columns(4)
            with col1 :
                 st.write("")
                 st.write("")
                 st.markdown("""                        
            <p><b>Accuracy = 0.32</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col2 :
                 st.markdown("""
            <p><b>Precision classe 0 = 0.33</b></p>
            <p><b>Precision classe 1 = 0.25</b></p>
                        <p><b>Precision classe 2 = 0.30</b></p>
                             <p><b>Precision classe 3 = 0.32</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col3:
                        st.markdown("""
            <p><b>Recall classe 0 = 0.67</b></p>
                        <p><b>Recall classe 1 = 0.00</b></p>
                        <p><b>Recall classe 2 = 0.34</b></p>
                        <p><b>Recall classe 3 = 0.19</b></p></div>
    """, unsafe_allow_html=True)
            with col4:
                        st.markdown("""
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 0 = 0.44</span><p>
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 1 = 0.00</span><p>
                  <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 2 = 0.32</span><p>
                   <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 3 = 0.24</span><p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Decision Tree Classifier multi-classes":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>Decision Tree Classifier</b></h4>""", unsafe_allow_html=True)
            col1,col2,col3, col4= st.columns(4)
            with col1 :
                 st.write("")
                 st.write("")
                 st.markdown("""                        
            <p><b>Accuracy = 0.40</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col2 :
                 st.markdown("""
            <p><b>Precision classe 0 = 0.51</b></p>
            <p><b>Precision classe 1 = 0.31</b></p>
                        <p><b>Precision classe 2 = 0.35</b></p>
                             <p><b>Precision classe 3 = 0.41</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col3:
                        st.markdown("""
            <p><b>Recall classe 0 = 0.51</b></p>
                        <p><b>Recall classe 1 = 0.31</b></p>
                        <p><b>Recall classe 2 = 0.35</b></p>
                        <p><b>Recall classe 3 = 0.40</b></p></div>
    """, unsafe_allow_html=True)
            with col4:
                        st.markdown("""
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 0 = 0.51</span><p>
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 1 = 0.13</span><p>
                  <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 2 = 0.36</span><p>
                   <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 3 = 0.40</span><p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Random Forest Classifier multi-classes":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>Random Forest Classifier</b></h4>""", unsafe_allow_html=True)
            col1,col2,col3, col4= st.columns(4)
            with col1 :
                 st.write("")
                 st.write("")
                 st.markdown("""                        
            <p><b>Accuracy = 0.42</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col2 :
                 st.markdown("""
            <p><b>Precision classe 0 = 0.50</b></p>
            <p><b>Precision classe 1 = 0.33</b></p>
                        <p><b>Precision classe 2 = 0.37</b></p>
                             <p><b>Precision classe 3 = 0.45</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col3:
                        st.markdown("""
            <p><b>Recall classe 0 = 0.60</b></p>
                        <p><b>Recall classe 1 = 0.27</b></p>
                        <p><b>Recall classe 2 = 0.37</b></p>
                        <p><b>Recall classe 3 = 0.41</b></p></div>
    """, unsafe_allow_html=True)
            with col4:
                        st.markdown("""
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 0 = 0.55</span><p>
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 1 = 0.30</span><p>
                  <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 2 = 0.37</span><p>
                   <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 3 = 0.43</span><p>
        </div>
    """, unsafe_allow_html=True)
            
            
        if choix == "XGB Classifier multi-classes":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>RXGB Classifierr</b></h4>""", unsafe_allow_html=True)
            col1,col2,col3, col4= st.columns(4)
            with col1 :
                 st.write("")
                 st.write("")
                 st.markdown("""                        
            <p><b>Accuracy = 0.42</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col2 :
                 st.markdown("""
            <p><b>Precision classe 0 = 0.39</b></p>
            <p><b>Precision classe 1 = 0.42</b></p>
                        <p><b>Precision classe 2 = 0.36</b></p>
                             <p><b>Precision classe 3 = 0.35</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col3:
                        st.markdown("""
            <p><b>Recall classe 0 = 0.41</b></p>
                        <p><b>Recall classe 1 = 0.66</b></p>
                        <p><b>Recall classe 2 = 0.08</b></p>
                        <p><b>Recall classe 3 = 0.38</b></p></div>
    """, unsafe_allow_html=True)
            with col4:
                        st.markdown("""
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 0 = 0.51</span><p>
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 1 = 0.13</span><p>
                  <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 2 = 0.36</span><p>
                   <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 3 = 0.40</span><p>
        </div>
    """, unsafe_allow_html=True)
            
            
        if choix == "KNN Classifier multi-classes":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>KNN Classifier</b></h4>""", unsafe_allow_html=True)
            
            col1,col2,col3, col4= st.columns(4)
            with col1 :
                 st.write("")
                 st.write("")
                 st.markdown("""                        
            <p><b>Accuracy = 0.28</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col2 :
                 st.markdown("""
            <p><b>Precision classe 0 = 0.31</b></p>
            <p><b>Precision classe 1 = 0.24</b></p>
                        <p><b>Precision classe 2 = 0.28</b></p>
                             <p><b>Precision classe 3 = 0.27</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col3:
                        st.markdown("""
            <p><b>Recall classe 0 = 0.45</b></p>
                        <p><b>Recall classe 1 = 0.21</b></p>
                        <p><b>Recall classe 2 = 0.23</b></p>
                        <p><b>Recall classe 3 = 0.20</b></p></div>
    """, unsafe_allow_html=True)
            with col4:
                        st.markdown("""
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 0 = 0.37</span><p>
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 1 = 0.22</span><p>
                  <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 2 = 0.25</span><p>
                   <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 3 = 0.23</span><p>
        </div>
    """, unsafe_allow_html=True)
            

        if choix == "Tableau comparatif et importance des variables multi-classes":
    
            st.write("")
            data = [[0.32, 0.33, 0.25, 0.30,0.32,0.67,0.00,0.34,0.19,0.44,0.00,0.32,0.24], [0.40, 0.51, 0.31, 0.35,0.41,0.51,0.32,0.35,0.40, 0.51,0.31,0.35,0.40],[0.42,0.50,0.33,0.37,0.45,0.60,0.27,0.37,0.41,0.55,0.3,0.37,0.43],[0.39, 0.42, 0.36,0.35,0.41, 0.66,0.08,0.38,0.39,0.51,0.13,0.36,0.40],[0.28, 0.31, 0.24, 0.28, 0.27,0.45,0.21,0.23,0.20,0.37,0.22,0.25,0.23]]  
            df3= pd.DataFrame(data, columns = ["ACCURACY", "PRECISION  Classe 0", "PRECISION Classe 1","PRECISION Classe 2","PRECISION Classe 3", "RECALL Classe 0", "RECALL Classe 1", "RECALL Classe 2", "RECALL Classe 3","F1 SCORE Classe 0","F1 SCORE Classe 1","F1 SCORE Classe 2","F1 SCORE Classe 3"], index =["Logistic Regression", "Decision Tree Classifier", "Random Forest Classifier", "XGB Classifier", "KNN Classifier"])
            df3_transposed = df3.T    
            st.markdown(df3_transposed.to_html(classes='medium-table'), unsafe_allow_html=True)
            st.markdown("""
        <style>
        .medium-table {
            font-size: 13px;
            text-align: center;
            margin-top: 10px;
            border-collapse: collapse;
        }
        .medium-table th, .medium-table td {
            padding: 6px 10px;
            border: 1px solid #ccc;
        }
        </style>
    """, unsafe_allow_html=True)
       
    

    with st.expander("🎯 **MODELES OPTIMISES**"):
        st.write("")
        st.markdown("Avec le **GridSearch**  et  **une  validation  croisée**, nous avons recherché les hyperparamètres optimisant notre modèle. Nous avons retenu :\n\n"
                "**max_depth à 20** (c’est-à-dire une profondeur de l’arbre de 20 nœuds au maximum)\n\n"
                "et **min_samples_split à 10** (c’est-à-dire un minimum de 10 échantillons requis pour séparer le nœud en 2")
        st.write("")
        st.markdown(
    "La métrique la plus pertinente pour notre jeu de données déséquilibré est "
    "<span style='color: #FF6961; font-weight: bold;'>F1-score</span>.",
    unsafe_allow_html=True
)
        st.markdown("Il reflète le mieux la qualité des prédictions positives")   
        st.write("")
        st.markdown("A partir de cette configuration de l'impact des variables explicatives," "nous avons décidé de garder les <span style='color: #FF6961; font-weight: bold;'> 6 premières variables les plus importantes</span> "  " dans le modèle optimisé final", unsafe_allow_html=True)

# Afficher le tableau avec style
        
        st.write("")
        st.write("")
        st.write("")
        col1,col2,col3= st.columns(3)
        with col2 :
            st.image("Importance_Multiclasses.png",width=600)
            st.write("")
              
        
        choix = st.radio("Sélectionnez un modèle",["Decision Tree Classifier multi-classes", "Random Forest Classifier multi-classes","Tableau comparatif"])  
    
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        if choix == "Decision Tree Classifier multi-classes":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>DECISION TREE CLASSIFIER MUTLI-CLASSES</b></h4>""", unsafe_allow_html=True)

            col1,col2,col3, col4= st.columns(4)
            with col1 :
                 st.write("")
                 st.write("")
                 st.markdown("""                        
            <p><b>Accuracy = 0.44</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col2 :
                 st.markdown("""
            <p><b>Precision classe 0 = 0.51</b></p>
            <p><b>Precision classe 1 = 0.34</b></p>
                        <p><b>Precision classe 2 = 0.38</b></p>
                             <p><b>Precision classe 3 = 0.51</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col3:
                        st.markdown("""
            <p><b>Recall classe 0 = 0.65</b></p>
                        <p><b>Recall classe 1 = 0.28</b></p>
                        <p><b>Recall classe 2 = 0.41</b></p>
                        <p><b>Recall classe 3 = 0.37</b></p></div>
    """, unsafe_allow_html=True)
            with col4:
                        st.markdown("""
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 0 = 0.57</span><p>
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 1 = 0.31</span><p>
                  <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 2 = 0.39</span><p>
                   <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 3 = 0.43</span><p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Random Forest Classifier multi-classes":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>RANDOM FOREST CLASSIFIER MUTLI-CLASSES</b></h4> """, unsafe_allow_html=True)

            col1,col2,col3, col4= st.columns(4)
            with col1 :
                 st.write("")
                 st.write("")
                 st.markdown("""                        
            <p><b>Accuracy = 0.47</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col2 :
                 st.markdown("""
            <p><b>Precision classe 0 = 0.56</b></p>
            <p><b>Precision classe 1 = 0.36</b></p>
                        <p><b>Precision classe 2 = 0.40</b></p>
                             <p><b>Precision classe 3 = 0.51</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col3:
                        st.markdown("""
            <p><b>Recall classe 0 = 0.65</b></p>
                        <p><b>Recall classe 1 = 0.32</b></p>
                        <p><b>Recall classe 2 = 0.40</b></p>
                        <p><b>Recall classe 3 = 0.46</b></p></div>
    """, unsafe_allow_html=True)
            with col4:
                        st.markdown("""
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 0 = 0.60</span><p>
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 1 = 0.33</span><p>
                  <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 2 = 0.40</span><p>
                   <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 3 = 0.49</span><p>
        </div>
    """, unsafe_allow_html=True)
                
        if choix == "Tableau comparatif":
            st.write("")
            st.write("")
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("<h5 style='margin-bottom: 10px;'>Decision Tree Classifier</h5>", unsafe_allow_html=True)
                data = [[0.44, 0.51, 0.65, 0.57], [0.44, 0.34, 0.28, 0.31], [0.44, 0.38, 0.41, 0.39],[0.44, 0.51, 0.37, 0.43]]  
                df4 = pd.DataFrame(data, columns = ["ACCURACY", "PRECISION", "RECALL", "F1 SCORE"], index =["Classe 0", "Classe 1", "Classe 2", "Classe 3"])
            
                
                def style_row(row):
                   html = "<tr>"
                   for col in df4.columns:
                        value = row[col]
                        if col == "F1 SCORE":
                            html += f"<td style='color:red; font-weight:bold; font-size:18px; text-align:center'>{value:.2f}</td>"
                        else:
                            html += f"<td style='font-size:16px; text-align:center'>{value:.2f}</td>"
                   html += "</tr>"
                   return html

# Génération du tableau HTML complet
                table_html = """
<style>
.custom-table {
    border-collapse: collapse;
    width: 100%;
}
.custom-table th {
    background-color: #f0f0f0;
    font-weight: bold;
    font-size: 18px;
    padding: 10px;
    text-align: center;
}
.custom-table td {
    padding: 10px;
    border: 1px solid #ccc;
}
</style>
<table class='custom-table'>
<tr>
    <th></th>
    <th>ACCURACY</th>
    <th>PRECISION</th>
    <th>RECALL</th>
    <th>F1 SCORE</th>
</tr>
"""
                for idx, row in df4.iterrows():
                   table_html += f"<tr><th style='text-align:center'>{idx}</th>" + style_row(row)[4:]  # Retirer <tr>
                table_html += "</table>"

# Affichage
                st.markdown(table_html, unsafe_allow_html=True)

            with col2:
                st.markdown("<h5 style='margin-bottom: 10px;'>Random Forest Classifier</h5>", unsafe_allow_html=True)
                data = [[0.47, 0.56, 0.65, 0.60], [0.47, 0.36, 0.32, 0.33], [0.47, 0.40, 0.40, 0.40],[0.47, 0.51, 0.46, 0.49]]  
                df5 = pd.DataFrame(data, columns = ["ACCURACY", "PRECISION", "RECALL", "F1 SCORE"], index =["Classe 0", "Classe 1", "Classe 2", "Classe 3"])
                
                def style_row(row):
                   html = "<tr>"
                   for col in df5.columns:
                        value = row[col]
                        if col == "F1 SCORE":
                            html += f"<td style='color:red; font-weight:bold; font-size:18px; text-align:center'>{value:.2f}</td>"
                        else:
                            html += f"<td style='font-size:16px; text-align:center'>{value:.2f}</td>"
                   html += "</tr>"
                   return html

# Génération du tableau HTML complet
                table_html = """
<style>
.custom-table {
    border-collapse: collapse;
    width: 100%;
}
.custom-table th {
    background-color: #f0f0f0;
    font-weight: bold;
    font-size: 18px;
    padding: 10px;
    text-align: center;
}
.custom-table td {
    padding: 10px;
    border: 1px solid #ccc;
}
</style>
<table class='custom-table'>
<tr>
    <th></th>
    <th>ACCURACY</th>
    <th>PRECISION</th>
    <th>RECALL</th>
    <th>F1 SCORE</th>
</tr>
"""
                for idx, row in df5.iterrows():
                   table_html += f"<tr><th style='text-align:center'>{idx}</th>" + style_row(row)[4:]  
                table_html += "</table>"
# Affichage
                st.markdown(table_html, unsafe_allow_html=True)


    

# === Page - Conclusion ===    
elif page == "Conclusion":
    st.markdown("<h1 style='text-align: center;'>Conclusion métier</h1>", unsafe_allow_html=True)
    st.image("Lfb_logo.jpg", width=100)
    st.write("")
    st.write("")
    st.markdown("""<div <style='font-size : 26px !important;'>Pour conclure, nous pouvons tirer plusieurs conclusions métiers utiles à la brigade:<br><br>
<ul>
 <li>Les <b>formulaires</b> contiennent énormément d’informations dont la plupart se répètent (plus de 25 colonnes sur les données GPS des incidents).
<li>Les temps de réponse sont <b>dans 75 % des cas inférieurs à 6 min</b>.
                </ul>
</div>""", unsafe_allow_html=True)
    st.write("")
    st.markdown("""<div <style='font-size : 26px !important;'>
 En France, toutes régions,le délai moyen d’intervention des pompiers après un appel est de <b>13 minutes</b>.<br><br>
 A Paris, le délai est de  <b>7 minutes</b> avec l'objectif  de rester sous la barre des <b>10 minutes</b>.<br><br>
 Il est important d’inscrire l’analyse des ces données dans une démarche de réévaluation et d’amélioration continue afin de toujours <b>garantir la sécurité des biens et des personnes</b>.  
                 </ul>
</div>""", unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    
    image = Image.open("LFB.png")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, width=250)

