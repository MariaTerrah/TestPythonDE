import unittest
import pandas as pd
from cleaning import format_date, clean_encoding, clean_spaces

class TestCleaningFunctions(unittest.TestCase):

    def test_clean_text_columns(self):
        df = pd.DataFrame({'title': ['Preemptive Infiltration With Betamethasone and Ropivacaine for Postoperative Pain in Laminoplasty or \xc3\xb1 Laminectomy']})
        df_cleaned = clean_encoding(df)
        expected_output = ['Preemptive Infiltration With Betamethasone and Ropivacaine for Postoperative Pain in Laminoplasty or Ã± Laminectomy']
        self.assertEqual(df_cleaned['title'].tolist(), expected_output)

    def test_clean_spaces(self):
        df = pd.DataFrame({'title': ['  Preemptive Infiltration', 'Laminectomy  ']})
        df= clean_spaces(df)
        expected_df = pd.DataFrame({'title': ['Preemptive Infiltration', 'Laminectomy']})
        self.assertTrue(df.equals(expected_df))

if __name__ == '__main__':
    unittest.main()
