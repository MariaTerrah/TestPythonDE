import unittest
from adhoc_processing import journal_with_most_drug_mentions, drugs_in_same_pubmed_journals

class TestAdhocProcessing(unittest.TestCase):

    def setUp(self):
        self.mentions_graph = {
            'Betamethasone': [
                {'journal': 'The journal of maternal-fetal & neonatal medicine', 'date': '2020-01-01', 'type': 'PubMed'},
                {'journal': 'Journal of back and musculoskeletal rehabilitation', 'date': '2020-01-01', 'type': 'PubMed'},
            ],
            'Atropine': [
                {'journal': 'The journal of maternal-fetal & neonatal medicine', 'date': '2020-01-03', 'type': 'PubMed'}
            ],
            'Isoprenaline': [
                {'journal': 'Journal of photochemistry and photobiology. B, Biology', 'date': '2020-01-01', 'type': 'PubMed'}
            ]
        }

    def test_journal_with_most_drug_mentions(self):
        journal, max = journal_with_most_drug_mentions(self.mentions_graph)
        self.assertEqual(journal, 'The journal of maternal-fetal & neonatal medicine')
        self.assertEqual(max, 2)

    def test_drugs_in_same_pubmed_journals(self):
        # Trouver les autres médicaments mentionnés dans les mêmes journaux que Betamethasone et seulement de type PubMed
        other_mentionned_drugs = drugs_in_same_pubmed_journals('Betamethasone', self.mentions_graph)
        expected_other_mentionned_drugs = {'Atropine'}  # Atropine est mentionné dans le même journal
        self.assertEqual(other_mentionned_drugs, expected_other_mentionned_drugs)

if __name__ == '__main__':
    unittest.main()
