from chp_client.query import build_onehop_query
import itertools
import tqdm
import logging
import pickle
import random
import json
from collections import defaultdict

from trapi_model.constants import *
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
queries = defaultdict(lambda: defaultdict(list))
disease = ['MONDO:0007254']
outcome_name = 'survival_time'
outcome = 'EFO:0000714'
outcome_op = '>'

# Build batch gene to disease query
for trapi_version in TRAPI_VERSIONS:
# Build batch gene wildcard and drug wildcard to disease query
    drug = [random.choice(list(curies["biolink:Drug"].keys()))]
    gene = [random.choice(list(curies["biolink:Gene"].keys()))]
    q = build_onehop_query(
            None,
            [BIOLINK_GENE, BIOLINK_DRUG],
            disease,
            [BIOLINK_DISEASE],
            outcome=outcome,
            outcome_op=outcome_op,
            outcome_value=random.randint(500,1500),
            trapi_version=trapi_version,
            drugs=drug,
            genes=gene,
            )
    print(q)
    input()
    queries[trapi_version]['batchwildcard_to_disease_proxy'] = q.to_dict()

# Pickle the queries
with open('wildcard_batch_onehop_queries.pk', 'wb') as f_:
    pickle.dump(dict(queries), f_)
