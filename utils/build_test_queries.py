""" Used for building queries that we know have inferences and probabilities.
"""
from chp_client import get_client
from chp_client.query import build_query
import itertools
import tqdm
import logging
import pickle

from chp.trapi_interface import TrapiInterface

import chp_client

print(chp_client.__file__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Get curies
logger.info('Getting curies.')
curies = TrapiInterface().get_curies()
#curies = client.curies()
logger.info('Got curies.')

# Build queries
queries = []

# One gene curie
queries.append(
    build_query(
        genes=['ENSEMBL:ENSG00000155657'],
        disease='MONDO:0007254',
        outcome=('EFO:0000714', '>=', 1000),
    )
)

# One gene one drug curie
queries.append(
    build_query(
        genes=['ENSEMBL:ENSG00000155657'],
        therapeutic='CHEMBL:CHEMBL83',
        disease='MONDO:0007254',
        outcome=('EFO:0000714', '>=', 1000),
    )
)

# Two gene one drug curie
queries.append(
    build_query(
        genes=['ENSEMBL:ENSG00000155657','ENSEMBL:ENSG00000241973'],
        therapeutic='CHEMBL:CHEMBL83',
        disease='MONDO:0007254',
        outcome=('EFO:0000714', '>=', 1000),
    )
)

# Pickle the queries
with open('test_reasoner_coulomb_queries.pk', 'wb') as f_:
    pickle.dump(queries, f_)
