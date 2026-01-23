#  Analyse Interactive des Ventes : Online Retail Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## 📋 Présentation du Projet
Ce projet transforme le dataset **Online Retail** de l'UCI Machine Learning Repository en un outil de Business Intelligence interactif. L'application permet d'explorer plus de 500 000 transactions réelles d'une boutique en ligne britannique, facilitant la prise de décision stratégique par la donnée.

****

---

## 🛠️ Pipeline de Traitement des Données
Le code intègre un moteur de nettoyage robuste pour garantir la précision des indicateurs :
* **Nettoyage :** Suppression automatique des `CustomerID` manquants et des doublons.
* **Filtrage Intelligent :** Élimination des valeurs aberrantes de quantité via la méthode des quartiles (Q1/Q3).
* **Feature Engineering :** Extraction granulaire des périodes (Heures, Jours, Semaines, Mois) et calcul dynamique du Revenu.
* **Gestion des Annulations :** Traitement spécifique des codes `InvoiceNo` commençant par "C".

---

##  Fonctionnalités Clés de l'Application

### 1. Tableau de Bord Exécutif (KPIs)
Aperçu instantané de la santé financière : Chiffre d'Affaires, Panier Moyen, Taux d'Annulation et de Retour.

### 2. Analyse Géographique Dynamique
Carte choroplèthe interactive permettant de visualiser la performance par pays avec des options de filtrage en temps réel dans la barre latérale.


### 3. Segmentation Client RFM
Calcul automatique des scores de **Récence, Fréquence et Montant** pour classer les clients en segments : *Champions, Fidèles, À risque, ou À perdre*.


### 4. Analyse de Pareto (80/20)
Visualisation combinée (Barres + Courbe de cumul) pour identifier les 20% de produits générant 80% du revenu total.


---

## 💻 Aperçu de l'Interface
*Prenez une capture d'écran de votre application lancée et remplacez le lien ci-dessous*
![Capture d'écran de l'application](https://via.placeholder.com/800x400?text=Aperçu+Streamlit+Online+Retail)

---

## ⚙️ Installation et Utilisation

### Prérequis
* Python 3.10+
* Le fichier `Online Retail.xlsx` à la racine du projet.

### Installation
1. Clonez le dépôt :
   ```bash
   git clone [https://github.com/Dave-kossi/online-retail-analysis.git](https://github.com/votre-nom/online-retail-analysis.git)
