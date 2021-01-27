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
import logging

from chp_client import get_client
from chp_client.query import build_query

logger = logging.getLogger(__name__)

#url = 'http://localhost:8000'
url = None

class TestClient(unittest.TestCase):
    """
    """

    def setUp(self):
        self.client = get_client(url=url)

    def test_predicates(self):
        """
        """
        preds = self.client.predicates()
        predicates_pretty = json.dumps(preds, indent=2)
        print(predicates_pretty)

    def test_curies(self):
        """
        """
        curies = self.client.curies()
        for entity_type, curies_dict in curies.items():
            logger.info('Number of curies for {} = {}'.format(entity_type, len(curies_dict)))

    def test_default(self):
        """
        """
        q = build_query( genes = ['ENSEMBL:ENSG00000132155'],
                         therapeutic='CHEMBL:CHEMBL88',
                         disease='MONDO:0007254',
                         outcome=('EFO:0000714', '>=', 1000) )
        r = self.client.query(q)
        prob = self.client.get_outcome_prob(r)
        print(prob)
        logger.info('Probability of survival',prob)

    def test_wildcard(self):
        """
        """
        q = build_query( therapeutic='CHEMBL:CHEMBL88',
                         disease='MONDO:0007254',
                         outcome=('EFO:0000714', '>=', 1000),
                         num_gene_wildcards=1 )
        r = self.client.query(q)
        prob = self.client.get_outcome_prob(r)
        print(prob)
        logger.info('Probability of survival',prob)
        ranked = self.client.get_ranked_wildcards(r)
        print(json.dumps(ranked, indent=2))

    def test_batch(self):
        """
        """
        queries = []
        for i in range(0, 10):
            q = build_query( genes = ['ENSEMBL:ENSG00000132155'],
                         therapeutic='CHEMBL:CHEMBL88',
                         disease='MONDO:0007254',
                         outcome=('EFO:0000714', '>=', 1000) )
            queries.append(q)
        for i in range(0, 3):
            q = build_query( therapeutic='CHEMBL:CHEMBL88',
                         disease='MONDO:0007254',
                         outcome=('EFO:0000714', '>=', 1000),
                         num_gene_wildcards=1 )
            queries.append(q)
        responses = self.client.query_all(queries)['message']
        for i in range(0, 10):
            prob = self.client.get_outcome_prob(responses[i])
            print('Probability of survival', prob)
        for i in range(10, 13):
            prob = self.client.get_outcome_prob(responses[i])
            ranked = self.client.get_ranked_wildcards(responses[i])
            print('Probability of survival', prob)
            print(json.dumps(ranked, indent=2))


if __name__ == '__main__':
    unittest.main()
