import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime, timedelta
import numpy as np

# === 1. CONFIGURATION ===
st.set_page_config(page_title="Analyse Online Retail", layout="wide", page_icon="📊")
st.title("📊 Analyse Complète - Dataset Online Retail")

# Palette de couleurs cohérente
COLOR_SEQ = px.colors.qualitative.Set3
COLOR_SCALE = px.colors.sequential.Blues

# === 2. CHARGEMENT ET NETTOYAGE DES DONNÉES ===
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Online Retail.xlsx")
        
        # Nettoyage des données
        df = df.dropna(subset=["CustomerID"])
        df = df[df["UnitPrice"] > 0]
        df = df.drop_duplicates()
        
        # Identifier les annulations (méthode exacte)
        df['Is_Cancellation'] = df["InvoiceNo"].astype(str).str.startswith("C")
        
        # Filtrer les quantités aberrantes (sauf pour les annulations)
        normal_transactions = df[~df['Is_Cancellation']]
        Q1 = normal_transactions['Quantity'].quantile(0.01)
        Q3 = normal_transactions['Quantity'].quantile(0.99)
        
        # Appliquer le filtre seulement aux transactions normales
        df_filtered = df[df['Is_Cancellation'] | ((df['Quantity'] >= Q1) & (df['Quantity'] <= Q3))]
        
        # Calculer le revenu
        df_filtered["Revenue"] = df_filtered["Quantity"] * df_filtered["UnitPrice"]
        
        # Ajouter des colonnes temporelles
        df_filtered['Year'] = df_filtered['InvoiceDate'].dt.year
        df_filtered['Month'] = df_filtered['InvoiceDate'].dt.month
        df_filtered['Month_Name'] = df_filtered['InvoiceDate'].dt.month_name()
        df_filtered['Day'] = df_filtered['InvoiceDate'].dt.day
        df_filtered['DayOfWeek'] = df_filtered['InvoiceDate'].dt.day_name()
        df_filtered['Hour'] = df_filtered['InvoiceDate'].dt.hour
        df_filtered['Week'] = df_filtered['InvoiceDate'].dt.isocalendar().week
        df_filtered['Week_Year'] = df_filtered['InvoiceDate'].dt.strftime('%Y-W%U')
        
        return df_filtered
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# === 3. FILTRES INTERACTIFS ===
st.sidebar.header("🔧 Filtres Interactifs")

# Filtre temporel
min_date = df["InvoiceDate"].min()
max_date = df["InvoiceDate"].max()
start_date, end_date = st.sidebar.date_input(
    "Sélectionnez une plage de dates",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filtre par pays avec option "Tous"
all_countries = sorted(df["Country"].unique())
selected_countries = st.sidebar.multiselect(
    "Sélectionnez les pays",
    options=["Tous"] + all_countries,
    default=["Tous"]
)

# Gérer la sélection "Tous"
if "Tous" in selected_countries:
    selected_countries = all_countries
else:
    selected_countries = [c for c in selected_countries if c != "Tous"]

# Appliquer les filtres
df_filtered = df[
    (df["InvoiceDate"] >= pd.to_datetime(start_date)) & 
    (df["InvoiceDate"] <= pd.to_datetime(end_date)) &
    (df["Country"].isin(selected_countries))
]

# === 4. SÉPARATION DES DONNÉES (MÉTHODE EXACTE) ===
# Identifier les annulations (méthode exacte)
annulation = df_filtered[df_filtered["InvoiceNo"].astype(str).str.startswith("C")]

# Identifier les retours
retours = df_filtered[(df_filtered["Quantity"] < 0) & (~df_filtered['Is_Cancellation'])]

# Identifier les ventes réelles
ventes = df_filtered[(df_filtered["Quantity"] > 0) & (~df_filtered['Is_Cancellation'])]

# === 5. KPI PRINCIPAUX ===
st.header("📈 Tableau de Bord Exécutif")

# Calcul des métriques
total_revenue = ventes["Revenue"].sum()
nb_orders = ventes["InvoiceNo"].nunique()
nb_customers = ventes["CustomerID"].nunique()
avg_basket = total_revenue / nb_orders if nb_orders > 0 else 0

nb_annulations = annulation["InvoiceNo"].nunique()
nb_produits_annules = abs(annulation["Quantity"].sum())
valeur_annulations = abs(annulation["Revenue"].sum())

ca_retours = abs(retours["Revenue"].sum()) if not retours.empty else 0
nb_retours = retours["InvoiceNo"].nunique() if not retours.empty else 0

# Affichage des KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("CA Total", f"{total_revenue:,.0f} £")
col2.metric("Commandes", f"{nb_orders:,}")
col3.metric("Clients", f"{nb_customers:,}")
col4.metric("Panier Moyen", f"{avg_basket:,.2f} £")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Annulations", f"{nb_annulations:,}")
col6.metric("Produits Annulés", f"{nb_produits_annules:,}")
col7.metric("Valeur Annulée", f"{valeur_annulations:,.0f} £")
col8.metric("Retours", f"{nb_retours:,}")

st.markdown("---")

# === 6. ANALYSE GÉOGRAPHIQUE ===
st.header("🌍 Analyse Géographique")

# CA par pays
country_revenue = ventes.groupby("Country")["Revenue"].sum().reset_index()
country_revenue = country_revenue.sort_values("Revenue", ascending=False)

col1, col2 = st.columns([2, 1])

with col1:
    # Top 10 pays par CA
    fig_top_countries = px.bar(
        country_revenue.head(10),
        x="Country", y="Revenue",
        title="Top 10 Pays par Chiffre d'Affaires",
        text_auto=".2s",
        color="Revenue",
        color_continuous_scale=COLOR_SCALE
    )
    st.plotly_chart(fig_top_countries, use_container_width=True)

with col2:
    # Carte mondiale du CA - MISE À JOUR POUR LA LOCALISATION
    if len(selected_countries) == 1:
        # Si un seul pays est sélectionné, on le met en évidence
        map_df = country_revenue.copy()
        map_df["Highlight"] = map_df["Country"].apply(
            lambda x: "Pays Sélectionné" if x == selected_countries[0] else "Autres Pays"
        )
        
        fig_world_map = px.choropleth(
            map_df,
            locations="Country",
            locationmode="country names",
            color="Highlight",
            title=f"Localisation de {selected_countries[0]}",
            color_discrete_map={
                "Pays Sélectionné": "red",
                "Autres Pays": "lightblue"
            },
            height=400
        )
    else:
        # Si multiple pays ou "Tous", carte normale
        fig_world_map = px.choropleth(
            country_revenue,
            locations="Country",
            locationmode="country names",
            color="Revenue",
            title="Répartition Géographique du CA",
            color_continuous_scale=COLOR_SCALE,
            height=400
        )
    
    st.plotly_chart(fig_world_map, use_container_width=True)

# === 7. PRODUITS LES PLUS PAYÉS PAR PAYS ===
st.header("💰 Produits les Plus Payés par Pays")

if len(selected_countries) <= 10:
    for country in selected_countries:
        st.subheader(f"🏆 Top 10 Produits - {country}")
        
        country_products = ventes[ventes["Country"] == country]
        top_products = country_products.groupby("Description")["Revenue"].sum().reset_index()
        top_products = top_products.sort_values("Revenue", ascending=False).head(10)
        
        if not top_products.empty:
            fig = px.bar(
                top_products,
                x="Description",
                y="Revenue",
                title=f"Top 10 Produits par CA - {country}",
                color="Revenue",
                color_continuous_scale=COLOR_SCALE,
                text="Revenue"
            )
            fig.update_traces(texttemplate='£%{y:,.0f}', textposition='outside')
            fig.update_layout(xaxis_tickangle=-45, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Tableau détaillé
            with st.expander(f"📋 Classement détaillé - {country}"):
                top_products_rank = top_products.copy()
                top_products_rank["Rank"] = range(1, len(top_products_rank) + 1)
                top_products_rank["Revenue"] = top_products_rank["Revenue"].round(2)
                st.dataframe(
                    top_products_rank[["Rank", "Description", "Revenue"]], 
                    use_container_width=True
                )
        else:
            st.info(f"Aucune donnée de vente pour {country}")

# === 8. ANALYSE PARETO DES PRODUITS ===
st.header("📊 Analyse Pareto des Produits")

# Analyse Pareto globale
pareto_df = ventes.groupby("Description")["Revenue"].sum().reset_index()
pareto_df = pareto_df.sort_values("Revenue", ascending=False)
pareto_df["cumperc"] = pareto_df["Revenue"].cumsum() / pareto_df["Revenue"].sum() * 100

fig_pareto = go.Figure()
fig_pareto.add_trace(go.Bar(
    x=pareto_df["Description"].head(20),
    y=pareto_df["Revenue"].head(20),
    name="CA par produit",
    marker_color=COLOR_SEQ[0]
))
fig_pareto.add_trace(go.Scatter(
    x=pareto_df["Description"].head(20),
    y=pareto_df["cumperc"].head(20),
    mode="lines+markers",
    name="% cumulé",
    yaxis="y2",
    line=dict(color=COLOR_SEQ[1])
))
fig_pareto.update_layout(
    title="Analyse de Pareto - Top 20 Produits",
    xaxis_title="Produits",
    yaxis=dict(title="CA (£)"),
    yaxis2=dict(title="% cumulé", overlaying="y", side="right"),
    showlegend=True,
    height=500
)
st.plotly_chart(fig_pareto, use_container_width=True)

# Détails Pareto
top_20_percent = pareto_df.head(int(len(pareto_df) * 0.2))
ca_top_20 = top_20_percent["Revenue"].sum()
percentage_top_20 = (ca_top_20 / total_revenue) * 100

st.info(f"**Règle des 80/20:** Les {len(top_20_percent)} produits du top 20% génèrent {percentage_top_20:.1f}% du CA total")

# === 9. ANALYSE DES ANNULATIONS PAR PAYS ===
st.header("🚫 Analyse des Annulations par Pays")

if not annulation.empty:
    # Nombre d'annulations par pays
    annulations_par_pays = (annulation.groupby("Country")["InvoiceNo"]
                                      .nunique()
                                      .sort_values(ascending=False)
                                      .reset_index()
                                      .rename(columns={"InvoiceNo": "Nb_annulations"}))
    
    # Graphique des annulations par pays
    fig_annulations_pays = px.bar(
        annulations_par_pays.head(15),
        x="Country",
        y="Nb_annulations",
        title="Top 15 Pays par Nombre d'Annulations",
        color="Nb_annulations",
        color_continuous_scale="reds",
        text="Nb_annulations"
    )
    fig_annulations_pays.update_traces(texttemplate='%{y}', textposition='outside')
    st.plotly_chart(fig_annulations_pays, use_container_width=True)
    
    # Carte des annulations - MISE À JOUR POUR LA LOCALISATION
    if len(selected_countries) == 1:
        # Si un seul pays est sélectionné
        annul_map_df = annulations_par_pays.copy()
        annul_map_df["Highlight"] = annul_map_df["Country"].apply(
            lambda x: "Pays Sélectionné" if x == selected_countries[0] else "Autres Pays"
        )
        
        fig_carte_annulations = px.choropleth(
            annul_map_df,
            locations="Country",
            locationmode="country names",
            color="Highlight",
            title=f"Annulations - Localisation de {selected_countries[0]}",
            color_discrete_map={
                "Pays Sélectionné": "red",
                "Autres Pays": "lightgrey"
            }
        )
    else:
        # Si multiple pays ou "Tous"
        fig_carte_annulations = px.choropleth(
            annulations_par_pays,
            locations="Country",
            locationmode="country names",
            color="Nb_annulations",
            title="Carte des Annulations par Pays",
            color_continuous_scale="reds"
        )
    
    st.plotly_chart(fig_carte_annulations, use_container_width=True)

# === 10. ANALYSE TEMPORELLE AVEC MOIS FRUCTUEUX ===
st.header("📅 Analyse Temporelle")

# === 10.1 MOIS LES PLUS FRUCTUEUX ===
st.subheader("💰 Mois les Plus Fructueux")

# Analyse par mois avec CA et nombre de commandes
mois_fructueux = ventes.groupby(['Year', 'Month', 'Month_Name']).agg({
    'Revenue': 'sum',
    'InvoiceNo': 'nunique',
    'CustomerID': 'nunique'
}).reset_index()

mois_fructueux = mois_fructueux.sort_values('Revenue', ascending=False)
mois_fructueux['Mois_Annee'] = mois_fructueux['Month_Name'] + ' ' + mois_fructueux['Year'].astype(str)

# Top 10 mois les plus fructueux
top_mois = mois_fructueux.head(10).copy()

fig_mois_fructueux = go.Figure()

fig_mois_fructueux.add_trace(go.Bar(
    x=top_mois['Mois_Annee'],
    y=top_mois['Revenue'],
    name='Chiffre d\'Affaires (£)',
    marker_color=COLOR_SEQ[0],
    text=top_mois['Revenue'],
    texttemplate='£%{text:,.0f}',
    textposition='outside'
))

fig_mois_fructueux.add_trace(go.Scatter(
    x=top_mois['Mois_Annee'],
    y=top_mois['InvoiceNo'],
    name='Nombre de Commandes',
    yaxis='y2',
    mode='lines+markers',
    line=dict(color=COLOR_SEQ[1], width=3),
    marker=dict(size=8)
))

fig_mois_fructueux.update_layout(
    title='Top 10 Mois les Plus Fructueux',
    xaxis_title='Mois',
    yaxis=dict(title='Chiffre d\'Affaires (£)', side='left'),
    yaxis2=dict(title='Nombre de Commandes', side='right', overlaying='y'),
    showlegend=True,
    xaxis_tickangle=-45,
    height=500
)

st.plotly_chart(fig_mois_fructueux, use_container_width=True)

# Tableau détaillé des mois fructueux
with st.expander("📋 Voir le détail complet des mois"):
    mois_display = mois_fructueux.copy()
    mois_display = mois_display.rename(columns={
        'Year': 'Année',
        'Month': 'Mois',
        'Month_Name': 'Nom_Mois',
        'Revenue': 'CA (£)',
        'InvoiceNo': 'Nb_Commandes',
        'CustomerID': 'Nb_Clients'
    })
    mois_display['CA (£)'] = mois_display['CA (£)'].round(2)
    st.dataframe(
        mois_display[['Année', 'Nom_Mois', 'CA (£)', 'Nb_Commandes', 'Nb_Clients']].sort_values('CA (£)', ascending=False),
        use_container_width=True,
        height=300
    )

# === 10.2 ÉVOLUTION TEMPORELLE ===
st.subheader("📈 Évolution Temporelle")

# Sélection de la période
periode = st.radio("Période d'analyse:", ["Hebdomadaire", "Mensuel", "Trimestriel", "Annuel"], horizontal=True)

# Préparation des données
df_temporel = ventes.set_index("InvoiceDate")

if periode == "Hebdomadaire":
    data_temporelle = df_temporel["Revenue"].resample("W").sum()
    data_commandes = df_temporel["InvoiceNo"].resample("W").nunique()
    title_periode = "Hebdomadaire"
    
elif periode == "Mensuel":
    data_temporelle = df_temporel["Revenue"].resample("M").sum()
    data_commandes = df_temporel["InvoiceNo"].resample("M").nunique()
    title_periode = "Mensuel"
    
elif periode == "Trimestriel":
    data_temporelle = df_temporel["Revenue"].resample("Q").sum()
    data_commandes = df_temporel["InvoiceNo"].resample("Q").nunique()
    title_periode = "Trimestriel"
    
else:
    data_temporelle = df_temporel["Revenue"].resample("Y").sum()
    data_commandes = df_temporel["InvoiceNo"].resample("Y").nunique()
    title_periode = "Annuel"

# Graphique d'évolution
fig_evolution = go.Figure()

fig_evolution.add_trace(go.Scatter(
    x=data_temporelle.index,
    y=data_temporelle.values,
    name='Chiffre d\'Affaires (£)',
    line=dict(color=COLOR_SEQ[0], width=3),
    yaxis='y'
))

fig_evolution.add_trace(go.Scatter(
    x=data_commandes.index,
    y=data_commandes.values,
    name='Nombre de Commandes',
    line=dict(color=COLOR_SEQ[1], width=2, dash='dash'),
    yaxis='y2'
))

fig_evolution.update_layout(
    title=f'Évolution du CA et des Commandes ({title_periode.lower()})',
    xaxis_title='Date',
    yaxis=dict(title='Chiffre d\'Affaires (£)', side='left'),
    yaxis2=dict(title='Nombre de Commandes', side='right', overlaying='y'),
    showlegend=True,
    hovermode='x unified'
)

st.plotly_chart(fig_evolution, use_container_width=True)

# === 10.3 STATISTIQUES TEMPORELLES ===
st.subheader("📊 Statistiques Temporelles")

col1, col2, col3, col4 = st.columns(4)

with col1:
    meilleur_mois_ca = mois_fructueux.iloc[0]
    st.metric("Meilleur Mois (CA)", 
              f"£{meilleur_mois_ca['Revenue']:,.0f}",
              f"{meilleur_mois_ca['Month_Name']} {meilleur_mois_ca['Year']}")

with col2:
    meilleur_mois_cmd = mois_fructueux.loc[mois_fructueux['InvoiceNo'].idxmax()]
    st.metric("Meilleur Mois (Commandes)", 
              f"{meilleur_mois_cmd['InvoiceNo']:,}",
              f"{meilleur_mois_cmd['Month_Name']} {meilleur_mois_cmd['Year']}")

with col3:
    ca_moyen_mensuel = mois_fructueux['Revenue'].mean()
    st.metric("CA Mensuel Moyen", f"£{ca_moyen_mensuel:,.0f}")

with col4:
    commandes_moyennes = mois_fructueux['InvoiceNo'].mean()
    st.metric("Commandes Mensuelles Moyennes", f"{commandes_moyennes:.0f}")

# === 11. ANALYSE DE SAISONNALITÉ ===
st.header("📈 Analyse de Saisonnalité")

col1, col2 = st.columns(2)

with col1:
    # Par jour de la semaine
    daily_revenue = ventes.groupby('DayOfWeek')['Revenue'].sum().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ])
    fig_daily = px.bar(daily_revenue.reset_index(), x='DayOfWeek', y='Revenue', 
                       title="CA par jour de la semaine",
                       color_discrete_sequence=[COLOR_SEQ[0]])
    st.plotly_chart(fig_daily, use_container_width=True)

with col2:
    # Par mois (moyenne sur toutes les années)
    ca_par_mois = ventes.groupby('Month_Name')['Revenue'].sum().reset_index()
    # Réordonner les mois
    order_mois = ['January', 'February', 'March', 'April', 'May', 'June', 
                 'July', 'August', 'September', 'October', 'November', 'December']
    ca_par_mois['Month_Name'] = pd.Categorical(ca_par_mois['Month_Name'], categories=order_mois, ordered=True)
    ca_par_mois = ca_par_mois.sort_values('Month_Name')
    
    fig_mois = px.bar(ca_par_mois, x='Month_Name', y='Revenue',
                     title="CA par mois (toutes années confondues)",
                     color_discrete_sequence=[COLOR_SEQ[1]])
    st.plotly_chart(fig_mois, use_container_width=True)

# === 12. ANALYSE RFM ===
st.header("👑 Analyse RFM (Récence-Fréquence-Monétaire) des Clients")

try:
    snapshot_date = ventes["InvoiceDate"].max() + pd.DateOffset(days=1)
    
    rfm_df = ventes.groupby("CustomerID").agg({
        "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
        "InvoiceNo": "nunique",
        "Revenue": "sum"
    }).rename(columns={
        "InvoiceDate": "Recency", 
        "InvoiceNo": "Frequency", 
        "Revenue": "Monetary"
    })
    
    if len(rfm_df) >= 4:
        rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'], 4, labels=range(4, 0, -1), duplicates='drop')
        rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'].rank(method='first'), 4, labels=range(1, 5), duplicates='drop')
        rfm_df['M_Score'] = pd.qcut(rfm_df['Monetary'], 4, labels=range(1, 5), duplicates='drop')
        
        rfm_df['R_Score'] = pd.to_numeric(rfm_df['R_Score'], errors='coerce')
        rfm_df['F_Score'] = pd.to_numeric(rfm_df['F_Score'], errors='coerce')
        rfm_df['M_Score'] = pd.to_numeric(rfm_df['M_Score'], errors='coerce')
        
        rfm_df['RFM_Score'] = rfm_df['R_Score'] + rfm_df['F_Score'] + rfm_df['M_Score']
        
        def segment_rfm(score):
            if pd.isna(score):
                return "Non classé"
            elif score >= 10:
                return "Champions"
            elif score >= 8:
                return "Clients Fidèles"
            elif score >= 6:
                return "Clients Prometteurs"
            elif score >= 4:
                return "Clients à Risque"
            else:
                return "Clients à Perdre"
        
        rfm_df['Segment'] = rfm_df['RFM_Score'].apply(segment_rfm)
        
        segment_counts = rfm_df['Segment'].value_counts().reset_index()
        fig_rfm = px.pie(segment_counts, values='count', names='Segment', 
                         title="Répartition des Segments Clients RFM",
                         color_discrete_sequence=COLOR_SEQ)
        st.plotly_chart(fig_rfm, use_container_width=True)
        
except Exception as e:
    st.error(f"Erreur dans l'analyse RFM: {e}")

# === 13. RECOMMANDATIONS STRATÉGIQUES ===
st.header("💡 Recommandations Stratégiques")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Actions Prioritaires")
    
    if not annulation.empty and nb_annulations > 0:
        st.warning("**Réduire les annulations**")
        st.write("- Analyser les causes des annulations")
        st.write("- Améliorer le processus de commande")
    
    top_product = pareto_df.iloc[0]['Description'] if not pareto_df.empty else "N/A"
    st.success(f"**Produit Phare:** {top_product}")
    st.write("- Développer des produits similaires")
    st.write("- Campagnes marketing ciblées")

with col2:
    st.subheader("📈 Opportunités")
    
    # Recommandations basées sur l'analyse temporelle
    meilleur_mois = mois_fructueux.iloc[0]
    st.info(f"**Période Forte:** {meilleur_mois['Month_Name']} {meilleur_mois['Year']}")
    st.write("- Préparer le stock à l'avance")
    st.write("- Renforcer le staffing pendant cette période")
    
    st.success("**Optimisation:**")
    st.write("- Focus sur le top 20% des produits")
    st.write("- Segmentation client RFM")

# === 14. EXPORT ET RAPPORT ===
st.markdown("---")
st.header("📤 Export des Données")

if st.button("📊 Générer Rapport Complet"):
    rapport = {
        "Période": f"{start_date} to {end_date}",
        "Pays": len(selected_countries),
        "CA Total": f"£{total_revenue:,.0f}",
        "Annulations": f"{nb_annulations}",
        "Top Produit": pareto_df.iloc[0]['Description'] if not pareto_df.empty else "N/A",
        "Top Pays": country_revenue.iloc[0]['Country'] if not country_revenue.empty else "N/A",
        "Meilleur Mois": f"{meilleur_mois_ca['Month_Name']} {meilleur_mois_ca['Year']} - £{meilleur_mois_ca['Revenue']:,.0f}"
    }
    
    st.success("Rapport généré!")
    st.json(rapport)

st.success("✅ Analyse complète terminée avec succès!")