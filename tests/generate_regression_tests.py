import itertools
import logging
import random
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

class QueryBuildingRegressionSuite:
    def __init__(self):
        # Edit these options to build a regression suite.
        # Multihop query options
        self.gene_options = [
                None,
                'GENE0001', 
                'GENE0002',
                ]
        self.drug_options = [
                None,
                'DRUG0001',
                'DRUG0002'
                ]
        self.disease_options = [
                None,
                'DIS0001',
                'DIS0001'
                ]
        self.outcome_options = [
                None,
                'OUT0001',
                'OUT0002',
                ]
        self.outcome_name_map = {
                "OUT0001": 'NAME001',
                "OUT0002": 'NAME002',
                None: None
                }
        self.outcome_op_options = {
                "OUT0001": ['==', '>', '<', 'matches'],
                "OUT0002": ['=='],
                None: None
                }
        self.outcome_value_options = {
                "OUT0001": (0, 10000),
                "OUT0002": [0,2,3],
                None: None,
                }
        self.trapi_version_options = [
                '1.0',
                '1.1',
                ]
        self.wildcard_options = [
                'biolink:Gene',
                'biolink:Drug',
                ]

        # Onehop query options
        self.q_object_category_options = [
                'biolink:Gene',
                'biolink:Drug',
                ]
        
        self.q_subject_category_options = [
                'biolink:Disease',
                'biolink:Gene',
                'biolink:Drug',
                ]

        self.q_category_map = {
                "biolink:Gene": [
                    'GENE0001',
                    'GENE0002',
                    ],
                "biolink:Drug": [
                    'DRUG0001',
                    'DRUG0001',
                    ],
                "biolink:Disease": [
                    'DIS0001',
                    'DIS0002',
                    ],
                }

        # Make class options
        self.build_class_options()

    def build_class_options(self):
        # Wrap None options
        self.outcome_op_options[None] = [None]
        self.outcome_value_options[None] = [None]

        # Make gene options
        new_gene_options = [None]
        self.gene_options.remove(None)
        for i in range(len(self.gene_options)):
            new_gene_options.append(self.gene_options[:i+1])
        self.gene_options = new_gene_options

        # Make drug options
        new_drug_options = [None]
        self.drug_options.remove(None)
        for i in range(len(self.drug_options)):
            new_drug_options.append(self.drug_options[:i+1])
        self.drug_options = new_drug_options
        logger.debug('Built class options.')

        # Build out 5 options for continuous value outcomes
        for outcome_value, options in self.outcome_value_options.items():
            if type(options) == tuple:
                self.outcome_value_options[outcome_value] = [random.randint(*options) for _ in range(3)]

    def get_options_iter(self, outcome, query_type):
        if query_type == 'standard':
            return itertools.product(
                self.gene_options,
                self.drug_options,
                self.disease_options,
                self.outcome_op_options[outcome],
                self.outcome_value_options[outcome],
                self.trapi_version_options,
                )
        elif query_type == 'wildcard':
            return itertools.product(
                self.wildcard_options,
                self.gene_options,
                self.drug_options,
                self.disease_options,
                self.outcome_op_options[outcome],
                self.outcome_value_options[outcome],
                self.trapi_version_options,
                )
        elif query_type == 'onehop':
            return itertools.product(
                    self.gene_options,
                    self.drug_options,
                    self.q_object_category_options,
                    self.q_subject_category_options,
                    self.outcome_op_options[outcome],
                    self.outcome_value_options[outcome],
                    self.trapi_version_options,
                    )
                    
        else:
            raise ValueError('Unrecognized query type: {}'.format(query_type))



    def make_standard_query_tests(self):
        tests = []
        logger.info('Building Standard Tests.')
        for outcome in self.outcome_options:
            outcome_name = self.outcome_name_map[outcome]
            outcome_iter = self.get_options_iter(outcome, 'standard')
            for option in outcome_iter:
                genes, drugs, disease,\
                    outcome_op, outcome_value, trapi_version = option
                test = {
                        "genes": genes,
                        "drugs": drugs,
                        "disease": disease,
                        "outcome": outcome,
                        "outcome_name": outcome_name,
                        "outcome_op": outcome_op,
                        "outcome_value": outcome_value,
                        "trapi_version": trapi_version,
                        }
                tests.append(test)
        return tests

    def make_wildcard_query_tests(self):
        tests = []
        logger.info('Building Wildcard Tests.')
        for outcome in self.outcome_options:
            outcome_name = self.outcome_name_map[outcome]
            outcome_iter = self.get_options_iter(outcome, 'wildcard')
            for option in outcome_iter:
                wildcard, genes, drugs, disease,\
                    outcome_op, outcome_value, trapi_version = option
                test = {
                        "wildcard_category": wildcard,
                        "genes": genes,
                        "drugs": drugs,
                        "disease": disease,
                        "outcome": outcome,
                        "outcome_name": outcome_name,
                        "outcome_op": outcome_op,
                        "outcome_value": outcome_value,
                        "trapi_version": trapi_version,
                        }
                tests.append(test)
        return tests

    def is_valid_onehop(self, 
            q_object,
            q_subject,
            genes,
            drugs,
            ):
        if genes is not None:
            if q_object in genes or q_subject in genes:
                return False
        if drugs is not None:
            if q_object in drugs or q_subject in drugs:
                return False
        return True

    def make_onehop_query_tests(self):
        tests = []
        logger.info('Building Onehop Tests.')
        for outcome in self.outcome_options:
            outcome_name = self.outcome_name_map[outcome]
            outcome_iter = self.get_options_iter(outcome, 'onehop')
            for option in outcome_iter:
                genes, drugs, q_object_category, q_subject_category,\
                    outcome_op, outcome_value, trapi_version = option
                if q_object_category == q_subject_category:
                    continue
                for q_subject, q_object in itertools.product(
                        self.q_category_map[q_object_category],
                        self.q_category_map[q_subject_category]
                        ):
                    if self.is_valid_onehop(
                            q_object,
                            q_subject, 
                            genes,
                            drugs,
                            ):
                        test = {
                                "genes": genes,
                                "drugs": drugs,
                                "q_object": q_object,
                                "q_object_category": q_object_category,
                                "q_subject": q_subject,
                                "q_subject_category": q_subject_category,
                                "outcome": outcome,
                                "outcome_name": outcome_name,
                                "outcome_op": outcome_op,
                                "outcome_value": outcome_value,
                                "trapi_version": trapi_version,
                            }
                        tests.append(test)
                    else:
                        logger.debug('Found invalid onehop')
        return tests

if __name__ == '__main__':
    tester = QueryBuildingRegressionSuite()
    standard_tests = tester.make_standard_query_tests()
    wildcard_tests = tester.make_wildcard_query_tests()
    onehop_tests = tester.make_onehop_query_tests()
    logger.info('Number of standard tests generate: {}'.format(len(standard_tests)))
    logger.info('Number of wildcard tests generate: {}'.format(len(wildcard_tests)))
    logger.info('Number of onehop tests generate: {}'.format(len(onehop_tests)))
    print('Complete')
