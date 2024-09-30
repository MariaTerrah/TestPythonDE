
import pandas as pd

# Fonction pour uniformiser le format des dates en 'YYYY-MM-DD'
def format_date(df, date_column):
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    df[date_column] = df[date_column].dt.strftime('%Y-%m-%d')
    return df


# Fonction pour corriger les problèmes d'encodage

def clean_encoding(df):
    def correct_encoding(text):
        try:
            text = bytes(text, 'utf-8').decode('unicode_escape')
            text = text.encode('latin1').decode('utf-8', errors='ignore')
        except (UnicodeDecodeError, TypeError): 
            pass
        return text

    # Appliquer la correction d'encodage sur les colonnes de type texte uniquement
    for column in df.columns:
        if df[column].dtype == 'object':  
            df[column] = df[column].apply(correct_encoding)

    return df


# Fonction pour enlever les espaces inutiles d'une colonne
def clean_spaces(df):
    for column in df.columns:
        if df[column].dtype == 'object':
            df[column] = df[column].str.strip() 
    return df
