# Python et Data Engineering

## Description
Ce projet met en place un data pipeline de traitement de données en Python pour nettoyer, transformer et analyser des mentions de médicaments dans des publications scientifiques et des essais cliniques. Le projet est structuré en plusieurs fichiers Python détaillés dans les parties ci-dessous.

Les étapes du projet incluent :
1. **Data cleansing** : 
Dans cette étape de cleansing , l'idée est d'appliquer un ensemble de traitement pour nettoyer et uniformiser la donnée :
    **1.1** Uniformisation du format des dates : les dates dans les fichiers ont plusieurs format différents ( 01/01/2019 , 2020-01-01 , "1 January 2020" ) donc il faut uniformiser le format pour pouvoir les traiter.
    **1.2** Gestion du mauvais encodage : exemple "Journal of emergency nursing\xc3\x28".
    **1.3** Suppression des espaces non nécéssaires.
    **1.4** Autres traitements possibles (non appliqués dans cet exercice): Gestion des valeurs nulles , gestion des doublons , gestion des caractères spéciaux.
2. **Data pipeline** : 
Création d'un graphe qui lie chaque médicament à ses mentions dans les différents journaux avec les dates et types de publication.
3. **Traitement ad-hoc** : 
Trouver le journal avec le plus de mentions de médicaments et les médicaments mentionnés dans les mêmes journaux PubMed.

## Organisation du projet

Le dossier **data** contient les fichiers de données JSON et CSV et le dossier **tests** contient les tests unitaires.
- **`cleaning.py`** : Contient les fonctions de cleansing citées dans la partie précédente.
- **`data_pipeline.py`** : Contient la partie de la génération du graphe de mentions.
- **`adhoc_processing.py`** : Contient la partie des traitements ad-hoc.
- **`main.py`** : Le point d'entrée principal du projet qui orchestre l'appel des autres fichiers.
- **`requirements.txt`** : Contient les dépendances du projet.


## Installation des dépendances nécessaires

pip3 install -r requirements.txt

## Exécution du projet 

python3 main.py

Résultat de l'exécution ci dessous: 
<img width="1061" alt="image" src="https://github.com/user-attachments/assets/b2f53e03-e11b-4f2f-90cc-96e577db4e87">


## Exécution des tests unitaires

python3 -m unittest discover -s tests

Résultat de l'exécution des tests ci-dessous;
<img width="1061" alt="image" src="https://github.com/user-attachments/assets/2875c548-8899-4d28-8dde-dd75198cfa96">


## Pour aller plus loin 

Eléments à considérer pour faire évoluer le code pour de grosses volumétries de données :

- **Partitionnement des données**  si la donnée est énorme cela peut être utile de partitionner par date par exemple ou autre(s) colonne(s) pertinentes
-**Orchestration des pipelines** avec Airflow par exemple pour organiser et automatiser l'exécution des tâches
- **Parallélisation** du traitement de données
- **Indexation** Créer des index sur les colonnes utilisées pour les filtres, les jointures afin d'accélérer les opérations de lecture et de recherche.
- **Logging , monitoring et gestion des erreurs** utiliser des logs et des outils de monitoring pour suivre les performances des data pipelines + intégrer une bonne gestion d'erreur pour éviter de bloquer le fonctionnement du pipeline
- **Caching** utiliser des systèmes de cache pour stocker les résultats intermédiaires d’un pipeline ou les données fréquemment consultées pour éviter de tout recalculer à chaque fois.

## SQL


**Première partie du test**

SELECT date , SUM(prod_price*prod_qty) FROM TRANSACTIONS
WHERE date BETWEEN '2020-01-01' AND '2020-12-31'
GROUP BY date
ORDER BY date ASC

**Seconde partie du test**

SELECT 
  t.client_id,
  SUM(CASE WHEN pn.product_type = 'MEUBLE' THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_meuble,
  SUM(CASE WHEN pn.product_type = 'DECO' THEN t.prod_price * t.prod_qty ELSE 0 END) AS ventes_deco
FROM 
  TRANSACTIONS t
JOIN 
  PRODUCT_NOMENCLATURE pn
ON 
  t.prod_id = pn.product_id
GROUP BY 
  t.client_id
;
