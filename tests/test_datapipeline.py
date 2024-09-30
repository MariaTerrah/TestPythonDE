import unittest
import pandas as pd
from data_pipeline import get_mentions_graph, load_mentions_graph
import json
import os

class TestDataPipeline(unittest.TestCase):

    def setUp(self):
        self.drugs_list = ['Betamethasone', 'Atropine']
        self.df_pubmed_json = pd.DataFrame({
            'title': ['Effects of Topical Application of Betamethasone on Imiquimod-induced Psoriasis-like Skin Inflammation in Mice.',
                      'Comparison of pressure BETAMETHASONE release, phonophoresis and dry needling in treatment of latent myofascial trigger point of upper trapezius ATROPINE muscle.'],
            'journal': ['Journal of back and musculoskeletal rehabilitation', 'The journal of maternal-fetal & neonatal medicine'],
            'date': ['2020-01-01', '2020-01-03']
        })
        self.df_list = [self.df_pubmed_json]
        self.titles = ['title']
        self.sources = ['PubMed']

    def test_get_mentions_graph(self):
        output_file = 'test_mentions_graph.json'
        get_mentions_graph(self.df_list, self.titles, self.drugs_list, self.sources, output_file)
        self.assertTrue(os.path.exists(output_file))

        with open(output_file, 'r') as f:
            graph = json.load(f)

        self.assertIn('Betamethasone', graph)
        self.assertEqual(len(graph['Betamethasone']), 2)
        self.assertEqual(graph['Betamethasone'][0]['journal'], 'Journal of back and musculoskeletal rehabilitation')


if __name__ == '__main__':
    unittest.main()
