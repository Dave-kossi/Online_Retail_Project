PRÉSENTATION
------------

Ce projet est une analyse exploratoire et approfondie (EDA) du jeu de données Online Retail (UCI Machine Learning Repository).

Il s’agit d’un jeu de données réel contenant :
* Les transactions d’une boutique en ligne basée au Royaume-Uni.
* Sur la période : décembre 2010 à décembre 2011.
* Volume de données : Plus de 500 000 lignes (achats, retours, clients, pays, etc.).

OBJECTIF : Explorer les données, identifier les tendances clés, comprendre le comportement des clients par pays et créer une application interactive avec Streamlit permettant de naviguer dans toutes les analyses.

NETTOYAGE DU DATASET
--------------------

Avant toute analyse, les données ont été soigneusement nettoyées et préparées :

* Suppression des valeurs manquantes sur les CustomerID.
* Suppression des doublons.
* Filtrage des transactions avec UnitPrice négatif ou nul.
* Identification et traitement des annulations (InvoiceNo commençant par 'C').
* Suppression des valeurs aberrantes sur les quantités.
* Ajout de nouvelles colonnes temporelles (Année, Mois, Jour, Heure, etc.).
* Calcul d’une colonne Revenue pour chaque transaction.

ANALYSES RÉALISÉES
-------------------

* KPI Exécutifs : CA total, nombre de commandes, nombre de clients, panier moyen, retours et annulations.
* Analyse géographique : Top pays par chiffre d’affaires et carte choroplèthe.
* Top produits par pays : Classement des 10 produits les plus générateurs de CA.
* Analyse de Pareto (80/20) : Identifier les produits qui génèrent 80 % du CA.
* Analyse temporelle : Mois les plus fructueux, évolution hebdomadaire/mensuelle/annuelle.
* Analyse de saisonnalité : CA par jour de la semaine et par mois.
* Analyse RFM (Récence-Fréquence-Monétaire) : Segmentation des clients.
* Recommandations stratégiques : Axées sur les insights obtenus.

TECHNOLOGIES UTILISÉES
-----------------------

* Python (3.10+)
* Pandas
* NumPy
* Plotly
* Streamlit
* openpyxl

LANCEMENT DE L'APPLICATION
--------------------------

Pour lancer l'application interactive :

streamlit run visual.py

RÉSULTATS CLÉS
--------------

* Identification des mois et jours les plus rentables.
* Découverte du top 10 des produits et pays les plus générateurs de CA.
* Vérification de la règle de Pareto (80/20) appliquée aux ventes.
* Segmentation RFM pour cibler les clients selon leur fidélité et leur valeur.
* Génération de recommandations business pour augmenter les ventes et réduire les annulations.
