# cleaning.py
import pandas as pd

# Fonction pour uniformiser le format des dates en 'YYYY-MM-DD'
def format_date(df, date_column):
    print(f"Formatting date column: {date_column}")
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce', format=None)
    df[date_column] = df[date_column].dt.strftime('%Y-%m-%d')
    return df

# Fonction pour corriger les problèmes d'encodage
def correct_encoding(text):
    if isinstance(text, str):
        try:
            text = bytes(text, 'utf-8').decode('unicode_escape')
            text = text.encode('latin1').decode('utf-8', errors='ignore')
        except UnicodeDecodeError:
            pass
    return text

# Fonction pour nettoyer les colonnes de type texte (str uniquement)
def clean_text_columns(df):
    print("Cleaning text columns")
    text_columns = df.select_dtypes(include=['object']).columns
    for column in text_columns:
        df[column] = df[column].apply(correct_encoding)
    return df

# Fonction pour enlever les espaces inutiles d'une colonne
def clean_text_column(column):
    print(f"Cleaning whitespace in column")
    return column.apply(lambda x: x.strip() if isinstance(x, str) else x)
