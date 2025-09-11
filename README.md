# 🛍️ Analyse Complète du Jeu de Données Online Retail

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit)
![Pandas](https://img.shields.io/badge/Lib-Pandas-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Lib-Plotly-3F4F75?logo=plotly)
![License](https://img.shields.io/badge/Licence-MIT-green)
![Status](https://img.shields.io/badge/Statut-En%20Cours-yellow)

## 📌 Présentation

Ce projet est une **analyse exploratoire et approfondie (EDA)** du jeu de données **Online Retail**, disponible sur le [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/online+retail).  
Il s’agit d’un jeu de données réel contenant :

- Les **transactions d’une boutique en ligne basée au Royaume-Uni**
- Sur la période **décembre 2010 à décembre 2011**
- Plus de **500 000 lignes** de données (achats, retours, clients, pays, etc.)

> 🎯 Objectif : Explorer les données, identifier les tendances clés, comprendre le comportement des clients et créer une **application interactive** permettant de naviguer dans toutes les analyses.

---

## 🧹 Nettoyage du Dataset

Avant toute analyse, les données ont été soigneusement nettoyées :

- Suppression des valeurs manquantes sur les `CustomerID`
- Suppression des doublons
- Filtrage des transactions avec `UnitPrice` négatif ou nul
- Identification et traitement des **annulations** (`InvoiceNo` commençant par `C`)
- Suppression des **valeurs aberrantes** sur les quantités
- Ajout de nouvelles colonnes temporelles (Année, Mois, Jour, Semaine, Jour de la semaine, Heure)
- Calcul d’une colonne `Revenue` pour chaque transaction
---

## 📊 Analyses Réalisées

- **KPI Exécutifs** : CA total, nombre de commandes, nombre de clients, panier moyen, retours et annulations
- **Analyse géographique** : Top pays par chiffre d’affaires et carte choroplèthe
- **Top produits par pays** : Classement des 10 produits les plus générateurs de CA
- **Analyse Pareto (80/20)** : Identifier les produits qui génèrent 80 % du CA
- **Analyse temporelle** : Mois les plus fructueux, évolution hebdomadaire/mensuelle/annuelle
- **Analyse de saisonnalité** : CA par jour de la semaine et par mois
- **Analyse RFM (Récence-Fréquence-Monétaire)** : Segmentation des clients
- **Recommandations stratégiques** : Axées sur les insights obtenus

---

## ⚙️ Technologies Utilisées

- [Python](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [Plotly](https://plotly.com/python/)
- [Streamlit](https://streamlit.io/)
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/) pour la lecture du fichier Excel

---

## 📁 Structure du Projet
├── visual.py # Script principal Streamlit
├── Online Retail.xlsx # Jeu de données source
├── requirements.txt # Dépendances du projet
└── README.md # Documentation

##Créer un environnement virtuel et installer les dépendances :
python -m venv venv
source venv/bin/activate      # Sur macOS / Linux
venv\Scripts\activate         # Sur Windows
pip install -r requirements.txt

## Lancement de l`application:
streamlit run visual.py
---
## 📌 Résultats Clés

#### Identification des mois et jours les plus rentables

#### Découverte du top 10 des produits et pays les plus générateurs de CA

#### Vérification de la règle de Pareto (80/20) appliquée aux ventes

#### Segmentation RFM pour cibler les clients selon leur fidélité et leur valeur

#### Génération de recommandations business pour augmenter les ventes et réduire les annulations

---

## 👤 Auteur

Ce projet a été conçu et réalisé par :

**Kossi Noumagno**  
🎓 Étudiant en Master Ingénierie Mathématique et Data Science  
📍 Université de Haute-Alsace (France) 
**LinkedIn :** [linkedin.com/in/kossi-noumagno](https://www.linkedin.com/in/kossi-noumagno/)  
**Portfolio :** [dave-kossi.github.io/mon_portfolio](https://dave-kossi.github.io/mon_portfolio/)  
**GitHub :** [github.com/Dave-kossi](https://github.com/Dave-kossi)

> 💡 N'hésitez pas à me contacter pour toute collaboration, opportunité professionnelle ou suggestion d'amélioration de ce projet.
