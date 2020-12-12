from chp_client import get_client
from multiprocessing import Pool
import pickle

LOCAL_URL = 'http://127.0.0.1:8000'

# Get local client
local_client = get_client(url=LOCAL_URL)

# Load in queries
print('Loading simple queries.')
with open('all_simple_queries.pk', 'rb') as f_:
    queries = pickle.load(f_)
print('Loaded simple queries.')

#local_client.query_all(queries[:10])

# Subset queries
TOTAL_QUERIES = len(queries)
TOTAL_WORKERS = 40
step = TOTAL_QUERIES // TOTAL_WORKERS
subset_queries = []
for i in range(0, TOTAL_QUERIES, step):
    subset_queries.append(queries[i:i+step])
print([len(subset) for subset in subset_queries])

def query_all(queries):
    local_client.query_all(queries)

input('Ready to run?')

pool = Pool(TOTAL_WORKERS)
pool.map(query_all, subset_queries)
