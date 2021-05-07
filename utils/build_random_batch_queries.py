from chp_client import get_client
from chp_client.query import build_standard_query
import itertools
import tqdm
import logging
import pickle
import random
import json

from chp.trapi_interface import TrapiInterface

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Set number of queries to build
NUM_QUERIES = 10

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
queries = []
for _ in range(NUM_QUERIES):
    genes = [gene for gene in random.choices(list(curies["biolink:Gene"].keys()), k=random.randint(0,1))]
    batch_genes = [gene for gene in random.choices(list(set(curies["biolink:Gene"].keys()) - set(genes)), k=random.randint(1,3))]
    drugs = [drug for drug in random.choices(list(curies["biolink:Drug"].keys()), k=random.randint(0,1))]
    batch_drugs = [drug for drug in random.choices(list(set(curies["biolink:Drug"].keys()) - set(drugs)), k=random.randint(1,3))]
    q = build_standard_query(
        genes=genes,
        drugs=drugs,
        disease='MONDO:0007254',
        outcome_name='survival_time',
        outcome='EFO:0000714', 
        outcome_op='>=',
        outcome_value=random.randint(1, 5000),
        trapi_version='1.0',
        batch_genes=batch_genes,
        batch_drugs=batch_drugs,
    )
    queries.append(q.to_dict())

# Pickle the queries
with open('random_batch_queries.pk', 'wb') as f_:
    pickle.dump(queries, f_)
