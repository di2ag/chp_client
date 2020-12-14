from chp_client import get_client
from chp_client.query import build_query
import itertools
import tqdm
import logging
import pickle
import numpy as np

from chp.trapi_interface import TrapiInterface

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Get curies
logger.info('Getting curies.')
curies = TrapiInterface().get_curies()
logger.info('Got curies.')

survival_times = list(np.linspace(350, 5000, 10))
genes = [gene for gene in curies["gene"]]

queries = []
for gene_curie in tqdm.tqdm(genes, desc='Building gene queries', leave=False):
    for st in survival_times:
        queries.append(
            build_query(
                genes=[gene_curie],
                disease='MONDO:0007254',
                outcome=('EFO:0000714', '>=', st),
            )
        )

# Pickle the queries
with open('simple_queries_1.pk', 'wb') as f_:
    pickle.dump(queries, f_)
