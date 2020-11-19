"""
    Source code developed by DI2AG.
    Thayer School of Engineering at Dartmouth College
    Authors:    Dr. Eugene Santos, Jr
                Mr. Chase Yakaboski,
                Mr. Gregory Hyde,
                Mr. Luke Veenhuis,
                Dr. Keum Joo Kim
"""

import unittest
import json
from chp_client import get_client
from chp_client.query import build_query

class TestClient(unittest.TestCase):
    """
    """

    def test_predicates(self):
        """
        """
        default_client = get_client()
        preds = default_client.predicates()
        predicates_pretty = json.dumps(preds, indent=2)
        print(predicates_pretty)

    def test_curies(self):
        """
        """
        default_client = get_client()
        curies = default_client.curies()
        print(curies.keys())
        for curie_type in curies.keys():
            term_length = min([len(curies[curie_type]),5])
            for curie in curies[curie_type][:term_length]:
                curie_pretty = json.dumps(curie, indent=2)
                print(curie_pretty)

    def test_default(self):
        """
        """
        default_client = get_client()
        q = build_query( genes = ['ENSEMBL:ENSG00000132155'],
                         therapeutic='CHEMBL:CHEMBL88',
                         disease='MONDO:0007254',
                         outcome=('EFO:0000714', '>=', 1000) )
        r = default_client.query(q)
        prob = default_client.get_outcome_prob(r)
        print('Probability of survival',prob)

    def test_wildcard(self):
        """
        """
        default_client = get_client()
        q = build_query( therapeutic='CHEMBL:CHEMBL88',
                         disease='MONDO:0007254',
                         outcome=('EFO:0000714', '>=', 1000),
                         num_gene_wildcards=1 )
        r = default_client.query(q)
        prob = default_client.get_outcome_prob(r)
        print('Probability of survival',prob)
        ranked = default_client.get_ranked_wildcards(r)
        print(json.dumps(ranked, indent=2))

if __name__ == '__main__':
    unittest.main()
