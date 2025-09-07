import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# === 1. Configuration ===
st.set_page_config(page_title="Analyse Online Retail", layout="wide")
st.title("📊 Analyse du jeu de données Online Retail")

# === 2. Chargement des données ===
@st.cache_data
def load_data():
    df = pd.read_excel("Online Retail.xlsx")
    df = df.dropna(subset=["CustomerID"])
    df = df[df["UnitPrice"] > 0]
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    return df

df = load_data()

ventes = df[df["Quantity"] > 0]
retours = df[df["Quantity"] < 0]

# === 3. KPIs de base ===
total_revenue = ventes["Revenue"].sum()
nb_orders = ventes["InvoiceNo"].nunique()
nb_customers = df["CustomerID"].nunique()
avg_basket = total_revenue / nb_orders

col1, col2, col3, col4 = st.columns(4)
col1.metric("CA total", f"{total_revenue:,.0f} £")
col2.metric("Nb commandes", nb_orders)
col3.metric("Nb clients", nb_customers)
col4.metric("Panier moyen", f"{avg_basket:,.2f} £")

st.markdown("---")

# === 4. Analyse Pareto ===
st.subheader("📈 Analyse de Pareto (Produits)")

pareto_df = ventes.groupby("Description")["Revenue"].sum().reset_index()
pareto_df = pareto_df.sort_values("Revenue", ascending=False)
pareto_df["cumperc"] = pareto_df["Revenue"].cumsum() / pareto_df["Revenue"].sum() * 100

fig_pareto = go.Figure()
fig_pareto.add_trace(go.Bar(
    x=pareto_df["Description"].head(30),
    y=pareto_df["Revenue"].head(30),
    name="CA par produit"
))
fig_pareto.add_trace(go.Scatter(
    x=pareto_df["Description"].head(30),
    y=pareto_df["cumperc"].head(30),
    mode="lines+markers",
    name="% cumulé",
    yaxis="y2"
))
fig_pareto.update_layout(
    title="Analyse de Pareto - Top 30 Produits",
    xaxis_title="Produits",
    yaxis=dict(title="CA"),
    yaxis2=dict(title="% cumulé", overlaying="y", side="right"),
    showlegend=True
)
st.plotly_chart(fig_pareto, use_container_width=True)

st.markdown("---")

# === 5. CA par pays ===
st.subheader("🌍 CA par pays")

country_df = ventes.groupby("Country")["Revenue"].sum().reset_index()
country_df = country_df.sort_values("Revenue", ascending=False).reset_index(drop=True)

# Catégories
country_df["Category"] = "Autres"
country_df.loc[country_df.index[:20], "Category"] = "Top 20"
country_df.loc[country_df.index[-10:], "Category"] = "Last 10"

# Sélecteur interactif
option = st.radio(
    "Choisir l'affichage des pays :",
    ("Tous", "Top 20", "Last 10"),
    horizontal=True
)

if option == "Top 20":
    map_df = country_df[country_df["Category"] == "Top 20"]
elif option == "Last 10":
    map_df = country_df[country_df["Category"] == "Last 10"]
else:
    map_df = country_df

# Top 10 bar chart
fig_country = px.bar(
    country_df.head(10),
    x="Country", y="Revenue",
    title="Top 10 pays par CA",
    text_auto=".2s",
    color="Revenue"
)

# Carte géographique
fig_map = px.choropleth(
    map_df,
    locations="Country",
    locationmode="country names",
    color="Category",
    title=f"CA par pays ({option})",
    color_discrete_map={
        "Top 20": "green",
        "Last 10": "red",
        "Autres": "lightgrey"
    }
)

col1, col2 = st.columns([2,1])
with col1:
    st.plotly_chart(fig_country, use_container_width=True)
with col2:
    st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")

# === 6. Taux de retours ===
st.subheader("🔄 Taux de retours")

ca_total = ventes["Revenue"].sum()
ca_retours = abs(retours["Revenue"].sum())
taux_retours_ca = (ca_retours / ca_total) * 100

nb_commandes_total = df["InvoiceNo"].nunique()
nb_commandes_retours = retours["InvoiceNo"].nunique()
taux_retours_cmd = (nb_commandes_retours / nb_commandes_total) * 100

nb_clients_total = df["CustomerID"].nunique()
nb_clients_retours = retours["CustomerID"].nunique()
taux_retours_clients = (nb_clients_retours / nb_clients_total) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Taux de retours (CA)", f"{taux_retours_ca:.2f}%")
col2.metric("Taux de retours (commandes)", f"{taux_retours_cmd:.2f}%")
col3.metric("Taux de retours (clients)", f"{taux_retours_clients:.2f}%")

kpi_retours = pd.DataFrame({
    "KPI": ["CA", "Commandes", "Clients"],
    "Taux_retours": [taux_retours_ca, taux_retours_cmd, taux_retours_clients]
})

fig_retours = px.bar(
    kpi_retours,
    x="KPI", y="Taux_retours",
    text="Taux_retours",
    title="Taux de retours (%)",
    color="KPI"
)
st.plotly_chart(fig_retours, use_container_width=True)
