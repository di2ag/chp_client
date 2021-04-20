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
import sys

from chp_client import get_client
from chp_client.query import build_standard_query, build_wildcard_query, build_onehop_query

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
#url = 'http://localhost:8000'
url = None

class TestQuery(unittest.TestCase):
    def test_build_standard_query(self):
        logger.info('Running TRAPI 1.0 Test.')
        q_1_0 = build_standard_query(
                genes=['ENSEMBL:ENSG00000132155'],
                drugs=['CHEMBL:CHEMBL88'],
                disease='MONDO:0007254',
                outcome='EFO:0000714',
                outcome_name='survival_time',
                outcome_op='>',
                outcome_value=600,
                trapi_version='1.0',
                )
        b, message = q_1_0.validate()
        if b is False:
            print(message)
        self.assertTrue(b)
        
        logger.info('Running TRAPI 1.1 test.')
        q_1_1 = build_standard_query(
                genes=['ENSEMBL:ENSG00000132155'],
                drugs=['CHEMBL:CHEMBL88'],
                disease='MONDO:0007254',
                outcome='EFO:0000714',
                outcome_name='survival_time',
                outcome_op='>',
                outcome_value=600,
                trapi_version='1.1',
                )
        b, message = q_1_1.validate()
        if b is False:
            print(message)
        self.assertTrue(b)
    
    def test_build_wildcard_query(self):
        logger.info('Running TRAPI 1.0 Test with gene wildcard.')
        q_1_0 = build_wildcard_query(
                'biolink:Gene',
                genes=['ENSEMBL:ENSG00000132155'],
                drugs=['CHEMBL:CHEMBL88'],
                disease='MONDO:0007254',
                outcome='EFO:0000714',
                outcome_name='survival_time',
                outcome_op='>',
                outcome_value=600,
                trapi_version='1.0',
                )
        b, message = q_1_0.validate()
        if b is False:
            print(message)
        self.assertTrue(b)
        
        logger.info('Running TRAPI 1.1 test with gene wildcard.')
        q_1_1 = build_wildcard_query(
                'biolink:Gene',
                genes=['ENSEMBL:ENSG00000132155'],
                drugs=['CHEMBL:CHEMBL88'],
                disease='MONDO:0007254',
                outcome='EFO:0000714',
                outcome_name='survival_time',
                outcome_op='>',
                outcome_value=600,
                trapi_version='1.1',
                )
        b, message = q_1_1.validate()
        if b is False:
            print(message)
        self.assertTrue(b)

        logger.info('Running TRAPI 1.0 Test with drug wildcard.')
        q_1_0 = build_wildcard_query(
                'biolink:Drug',
                genes=['ENSEMBL:ENSG00000132155'],
                drugs=['CHEMBL:CHEMBL88'],
                disease='MONDO:0007254',
                outcome='EFO:0000714',
                outcome_name='survival_time',
                outcome_op='>',
                outcome_value=600,
                trapi_version='1.0',
                )
        b, message = q_1_0.validate()
        if b is False:
            print(message)
        self.assertTrue(b)
        
        logger.info('Running TRAPI 1.1 test with drug wildcard.')
        q_1_1 = build_wildcard_query(
                'biolink:Drug',
                genes=['ENSEMBL:ENSG00000132155'],
                drugs=['CHEMBL:CHEMBL88'],
                disease='MONDO:0007254',
                outcome='EFO:0000714',
                outcome_name='survival_time',
                outcome_op='>',
                outcome_value=600,
                trapi_version='1.1',
                )
        b, message = q_1_1.validate()
        if b is False:
            print(message)
        self.assertTrue(b)

    def test_build_onehop_standard_query(self):
        logger.info('Running TRAPI 1.0 Test with gene to drug.')
        q_1_0 = build_onehop_query(
                q_subject='ENSEMBL:ENSG00000132155',
                q_subject_category = 'biolink:Gene',
                q_object='CHEMBL:CHEMBL88',
                q_object_category='biolink:Drug',
                outcome='EFO:0000714',
                outcome_name='survival_time',
                outcome_op='>',
                outcome_value=600,
                trapi_version='1.0',
                )
        b, message = q_1_0.validate()
        if b is False:
            print(message)
        self.assertTrue(b)
        
        logger.info('Running TRAPI 1.1 Test with gene to drug.')
        q_1_0 = build_onehop_query(
                q_subject='ENSEMBL:ENSG00000132155',
                q_subject_category = 'biolink:Gene',
                q_object='CHEMBL:CHEMBL88',
                q_object_category='biolink:Drug',
                outcome='EFO:0000714',
                outcome_name='survival_time',
                outcome_op='>',
                outcome_value=600,
                trapi_version='1.1',
                )
        b, message = q_1_0.validate()
        if b is False:
            print(message)
        self.assertTrue(b)

        logger.info('Running TRAPI 1.0 Test with drug to gene.')
        q_1_0 = build_onehop_query(
                q_object='ENSEMBL:ENSG00000132155',
                q_object_category = 'biolink:Gene',
                q_subject='CHEMBL:CHEMBL88',
                q_subject_category='biolink:Drug',
                outcome='EFO:0000714',
                outcome_name='survival_time',
                outcome_op='>',
                outcome_value=600,
                trapi_version='1.0',
                )
        b, message = q_1_0.validate()
        if b is False:
            print(message)
        self.assertTrue(b)
        
        logger.info('Running TRAPI 1.1 Test with drug to gene.')
        q_1_0 = build_onehop_query(
                q_object='ENSEMBL:ENSG00000132155',
                q_object_category = 'biolink:Gene',
                q_subject='CHEMBL:CHEMBL88',
                q_subject_category='biolink:Drug',
                outcome='EFO:0000714',
                outcome_name='survival_time',
                outcome_op='>',
                outcome_value=600,
                trapi_version='1.1',
                )
        b, message = q_1_0.validate()
        if b is False:
            print(message)
        self.assertTrue(b)

        logger.info('Running TRAPI 1.0 Test with drug to disease.')
        q_1_0 = build_onehop_query(
                q_object='MONDO:0007254',
                q_object_category = 'biolink:Disease',
                q_subject='CHEMBL:CHEMBL88',
                q_subject_category='biolink:Drug',
                outcome='EFO:0000714',
                outcome_name='survival_time',
                outcome_op='>',
                outcome_value=600,
                trapi_version='1.0',
                )
        b, message = q_1_0.validate()
        if b is False:
            print(message)
        self.assertTrue(b)
        
        logger.info('Running TRAPI 1.1 Test with drug to disease.')
        q_1_0 = build_onehop_query(
                q_object='MONDO:0007254',
                q_object_category = 'biolink:Disease',
                q_subject='CHEMBL:CHEMBL88',
                q_subject_category='biolink:Drug',
                outcome='EFO:0000714',
                outcome_name='survival_time',
                outcome_op='>',
                outcome_value=600,
                trapi_version='1.1',
                )
        b, message = q_1_0.validate()
        if b is False:
            print(message)
        self.assertTrue(b)

        logger.info('Running TRAPI 1.0 Test with gene to disease.')
        q_1_0 = build_onehop_query(
                q_object='MONDO:0007254',
                q_object_category = 'biolink:Disease',
                q_subject='ENSEMBL:ENSG00000132155',
                q_subject_category = 'biolink:Gene',
                outcome='EFO:0000714',
                outcome_name='survival_time',
                outcome_op='>',
                outcome_value=600,
                trapi_version='1.0',
                )
        b, message = q_1_0.validate()
        if b is False:
            print(message)
        self.assertTrue(b)

        logger.info('Running TRAPI 1.1 Test with gene to disease.')
        q_1_0 = build_onehop_query(
                q_object='MONDO:0007254',
                q_object_category = 'biolink:Disease',
                q_subject='ENSEMBL:ENSG00000132155',
                q_subject_category = 'biolink:Gene',
                outcome='EFO:0000714',
                outcome_name='survival_time',
                outcome_op='>',
                outcome_value=600,
                trapi_version='1.1',
                )
        b, message = q_1_0.validate()
        if b is False:
            print(message)
        self.assertTrue(b)

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
