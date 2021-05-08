from chp_client import get_client
from chp_client.query import build_standard_query
import itertools
import tqdm
import logging
import pickle
import random
import json
from collections import defaultdict

from chp.trapi_interface import TrapiInterface

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Set number of queries to build
NUM_QUERIES = 10

TRAPI_VERSIONS = ['1.0', '1.1']

# Set seed
random.seed(111)

# Get client
#client = get_client()

# Get curies
logger.info('Getting curies.')
curies = TrapiInterface().get_curies()
#curies = client.curies()
logger.info('Got curies.')

# Build all simple single gene, single drug, breast cancer, survival queries.
queries = defaultdict(list)
for trapi_version in TRAPI_VERSIONS:
    for _ in range(NUM_QUERIES):
        genes = [gene for gene in random.choices(list(curies["biolink:Gene"].keys()), k=random.randint(1,3))]
        therapeutic=random.choice(list(curies["biolink:Drug"].keys()))
        q = build_standard_query(
            genes=genes,
            drugs=[therapeutic],
            disease='MONDO:0007254',
            outcome_name='survival_time',
            outcome='EFO:0000714', 
            outcome_op='>',
            outcome_value=random.randint(1, 5000),
            trapi_version=trapi_version,
        )
        queries[trapi_version].append(q.to_dict())

# Pickle the queries
with open('random_queries.pk', 'wb') as f_:
    pickle.dump(queries, f_)
