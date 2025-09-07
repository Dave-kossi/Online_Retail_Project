# === 1. Import des librairies ===
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# === 2. Chargement des données ===
df = pd.read_excel("Online Retail.xlsx")  # adapter le chemin

# === 3. Nettoyage des données ===
df = df.dropna(subset=["CustomerID"])  # enlever clients inconnus
df = df[df["Quantity"] > 0]             # enlever retours
df = df[df["UnitPrice"] > 0]            # enlever prix négatifs

# Créer une colonne Chiffre d'Affaires
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# === 4. KPI de base ===
total_revenue = df["Revenue"].sum()
nb_orders = df["InvoiceNo"].nunique()
nb_customers = df["CustomerID"].nunique()
avg_basket = total_revenue / nb_orders

print("CA total : ", round(total_revenue,2))
print("Nombre de commandes : ", nb_orders)
print("Nombre de clients : ", nb_customers)
print("Panier moyen : ", round(avg_basket,2))

# === 5. Loi de Pareto (80/20) ===
pareto_df = df.groupby("Description")["Revenue"].sum().reset_index()
pareto_df = pareto_df.sort_values("Revenue", ascending=False)
pareto_df["cumperc"] = pareto_df["Revenue"].cumsum() / pareto_df["Revenue"].sum() * 100

# Graphique Pareto
fig_pareto = go.Figure()

# Barres (CA par produit)
fig_pareto.add_trace(go.Bar(
    x=pareto_df["Description"],
    y=pareto_df["Revenue"],
    name="CA par produit"
))

# Courbe cumulée
fig_pareto.add_trace(go.Scatter(
    x=pareto_df["Description"],
    y=pareto_df["cumperc"],
    mode="lines+markers",
    name="% cumulé"
))

fig_pareto.update_layout(
    title="Analyse de Pareto - Produits (80/20)",
    xaxis_title="Produits",
    yaxis_title="Chiffre d'Affaires",
    yaxis2=dict(title="% cumulé", overlaying="y", side="right"),
    showlegend=True
)

fig_pareto.show()

# === 6. CA par pays ===
country_df = df.groupby("Country")["Revenue"].sum().reset_index()
country_df = country_df.sort_values("Revenue", ascending=False)

fig_country = px.bar(
    country_df.head(10),
    x="Country",
    y="Revenue",
    title="Top 10 pays par Chiffre d'Affaires",
    text_auto=".2s"
)
fig_country.show()

# === 7. Carte géographique (optionnel) ===
fig_map = px.choropleth(
    country_df,
    locations="Country",
    locationmode="country names",
    color="Revenue",
    title="CA par pays (carte mondiale)"
)
fig_map.show()
