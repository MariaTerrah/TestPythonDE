import pandas as pd
import json

# Fonction pour uniformiser le format des dates en 'YYYY-MM-DD'
def format_date(df, date_column):
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
    text_columns = df.select_dtypes(include=['object']).columns
    for column in text_columns:
        df[column] = df[column].apply(correct_encoding)
    return df

# Fonction pour enlever les espaces inutiles d'une colonne
def clean_text_column(column):
    return column.apply(lambda x: x.strip() if isinstance(x, str) else x)

# Fonction pour trouver les mentions de médicaments et générer un fichier JSON en sortie
def get_mentions_graph(df_list, titles, drugs_list, sources, output_file):
    mentions_graph = {}
    for df, title, source in zip(df_list, titles, sources):
        for drug in drugs_list:
            matches = df[df[title].str.contains(drug, case=False, na=False)]
            for _, row in matches.iterrows():
                if drug not in mentions_graph:
                    mentions_graph[drug] = []
                mentions_graph[drug].append({
                    'journal': row['journal'],
                    'date': row['date'],
                    'title': row[title],
                    'type': source  # soit PubMed ou Clinical Trials
                })

    with open(output_file, 'w') as json_file:
        json.dump(mentions_graph, json_file, indent=4)

    print(f"Fichier JSON généré : {output_file}")

# Fonction pour charger le graphe des mentions depuis un fichier JSON
def load_mentions_graph(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

# Fonction pour trouver le journal qui mentionne le plus de médicaments
def journal_with_most_drug_mentions(mentions_graph):
    journal_dict = {}
    for drug, mentions in mentions_graph.items():
        for mention in mentions:
            journal = mention['journal']
            if journal not in journal_dict:
                journal_dict[journal] = set()  # pour l'unicité des éléments
            journal_dict[journal].add(drug)
    
    max_drugs_journal = max(journal_dict, key=lambda j: len(journal_dict[j]))
    return max_drugs_journal, len(journal_dict[max_drugs_journal])

# Fonction pour trouver les autres médicaments mentionnés dans les mêmes journaux PubMed mais pas dans Clinical Trials
def drugs_in_same_pubmed_journals(drug, mentions_graph):
    pubmed_journals = set()
    if drug in mentions_graph:
        for mention in mentions_graph[drug]:
            if mention['type'] == 'PubMed':
                pubmed_journals.add(mention['journal'])
    
    other_mentioned_drugs = set()
    for other_drug, mentions in mentions_graph.items():
        if other_drug != drug:
            for mention in mentions:
                if mention['journal'] in pubmed_journals and mention['type'] == 'PubMed':
                    other_mentioned_drugs.add(other_drug)
    
    return other_mentioned_drugs

# Fonction principale pour charger et traiter les données
def main():
    # Charger les fichiers de données
    drugs_df = pd.read_csv('drugs.csv')
    clinical_trials_df = pd.read_csv('clinical_trials.csv', encoding='utf-8')
    pubmed_csv_df = pd.read_csv('pubmed.csv')
    
    with open('pubmed.json', 'r') as f:
        pubmed_json_df = pd.DataFrame(json.load(f))

    # Nettoyer et traiter les données
    clinical_trials_df = format_date(clinical_trials_df, 'date')
    pubmed_csv_df = format_date(pubmed_csv_df, 'date')
    pubmed_json_df = format_date(pubmed_json_df, 'date')
    
    clinical_trials_df = clean_text_columns(clinical_trials_df)
    pubmed_csv_df = clean_text_columns(pubmed_csv_df)
    pubmed_json_df = clean_text_columns(pubmed_json_df)
    
    clinical_trials_df['scientific_title'] = clean_text_column(clinical_trials_df['scientific_title'])
    pubmed_csv_df['title'] = clean_text_column(pubmed_csv_df['title'])
    pubmed_json_df['title'] = clean_text_column(pubmed_json_df['title'])
    drugs_df['drug'] = clean_text_column(drugs_df['drug'])
    
    # Générer le graphe des mentions et sauvegarder dans un fichier JSON
    drug_names = drugs_df['drug'].tolist()
    df_list = [clinical_trials_df, pubmed_csv_df, pubmed_json_df]
    titles = ['scientific_title', 'title', 'title']
    sources = ['ClinicalTrials', 'PubMed', 'PubMed']
    get_mentions_graph(df_list, titles, drug_names, sources, 'mentions_graph_output.json')
    
    # Charger le graphe des mentions et trouver le journal avec le plus de mentions de médicaments
    mentions_graph = load_mentions_graph('mentions_graph_output.json')
    journal, count = journal_with_most_drug_mentions(mentions_graph)
    print(f"Le journal qui mentionne le plus de médicaments est : {journal} avec {count} médicaments mentionnés.")
    
    # Exemple pour trouver d'autres médicaments mentionnés dans les mêmes journaux que "TETRACYCLINE" (uniquement PubMed)
    drug = 'TETRACYCLINE'
    other_mentioned_drugs = drugs_in_same_pubmed_journals(drug, mentions_graph)
    print(f"Les médicaments mentionnés dans les mêmes journaux que {drug} (uniquement PubMed) sont : {other_mentioned_drugs}")

if __name__ == '__main__':
    main()
