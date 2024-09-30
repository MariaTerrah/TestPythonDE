# main.py
import pandas as pd
import json
from cleaning import format_date, clean_text_columns, clean_text_column
from data_pipeline import get_mentions_graph, load_mentions_graph
from adhoc_processing import journal_with_most_drug_mentions, drugs_in_same_pubmed_journals

def main():
    print("Starting the data processing pipeline...")

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
