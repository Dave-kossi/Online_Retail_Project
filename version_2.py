import pandas as pd
from ydata_profiling import ProfileReport
import os
import webbrowser


# ===============================
# 1. Chargement du dataset
# ===============================
def charger_donnees(fichier: str) -> pd.DataFrame:
    extension = os.path.splitext(fichier)[-1].lower()

    if extension == ".csv":
        return pd.read_csv(fichier)
    elif extension in [".xls", ".xlsx"]:
        return pd.read_excel(fichier)
    elif extension == ".json":
        return pd.read_json(fichier)
    elif extension == ".parquet":
        return pd.read_parquet(fichier)
    elif extension == ".txt":
        return pd.read_csv(fichier, delimiter="\t")
    else:
        raise ValueError(f"Extension de fichier non supportée : {extension}")


# ===============================
# 2. Nettoyage automatique
# ===============================
def nettoyer_donnees(df: pd.DataFrame) -> pd.DataFrame:
    # Supprimer les doublons
    df = df.drop_duplicates()

    # Nettoyer les noms de colonnes
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Conversion automatique des types (numériques / dates si possible)
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass  # garder tel quel si conversion impossible

    # Gestion des valeurs manquantes :
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col].fillna(df[col].median(), inplace=True)
            else:
                df[col].fillna("inconnu", inplace=True)

    return df


# ===============================
# 3. Sauvegarde du dataset nettoyé
# ===============================
def sauvegarder_donnees(df: pd.DataFrame, fichier_entree: str) -> str:
    extension = os.path.splitext(fichier_entree)[-1].lower()
    sortie = "donnees_nettoyees" + extension

    if extension == ".csv":
        df.to_csv(sortie, index=False)
    elif extension in [".xls", ".xlsx"]:
        df.to_excel(sortie, index=False)
    elif extension == ".json":
        df.to_json(sortie, orient="records", force_ascii=False)
    elif extension == ".parquet":
        df.to_parquet(sortie, index=False)
    elif extension == ".txt":
        df.to_csv(sortie, index=False, sep="\t")
    else:
        raise ValueError(f"Extension de fichier non supportée : {extension}")

    return sortie


# ===============================
# 4. Programme principal
# ===============================
def main():
    fichier = input("👉 Entrez le chemin de votre fichier : ").strip()
    fichier = os.path.abspath(fichier)

    base_sortie = input("👉 Préfixe des rapports [rapport] : ").strip() or "rapport"

    try:
        if not os.path.exists(fichier):
            raise FileNotFoundError(f"Le fichier {fichier} n'existe pas.")

        # Étape 1 : Chargement
        df = charger_donnees(fichier)
        if df.empty:
            raise ValueError("Le fichier est vide.")
        print(f"✅ Dataset chargé : {df.shape[0]} lignes, {df.shape[1]} colonnes")

        # Étape 2 : Audit AVANT nettoyage
        rapport_avant = f"{base_sortie}_avant.html"
        profile_avant = ProfileReport(df, title="Audit AVANT Nettoyage", explorative=True, minimal=False)
        profile_avant.to_file(rapport_avant)
        print(f"📊 Rapport AVANT nettoyage généré : {rapport_avant}")

        # Étape 3 : Nettoyage
        df_clean = nettoyer_donnees(df)
        print(f"🧹 Données nettoyées : {df_clean.shape[0]} lignes, {df_clean.shape[1]} colonnes")

        # Étape 4 : Sauvegarde du dataset propre
        fichier_nettoye = sauvegarder_donnees(df_clean, fichier)
        print(f"💾 Données nettoyées sauvegardées dans : {fichier_nettoye}")

        # Étape 5 : Audit APRES nettoyage
        rapport_apres = f"{base_sortie}_apres.html"
        profile_apres = ProfileReport(df_clean, title="Audit APRES Nettoyage", explorative=True, minimal=False)
        profile_apres.to_file(rapport_apres)
        print(f"📊 Rapport APRES nettoyage généré : {rapport_apres}")

        # Étape 6 : Ouvrir les rapports automatiquement
        webbrowser.open(rapport_avant)
        webbrowser.open(rapport_apres)

    except Exception as e:
        print(f"❌ Erreur : {e}")


if __name__ == "__main__":
    main()
