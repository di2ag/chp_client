from chp_client import get_client
from multiprocessing import Pool
import pickle
import json

LOCAL_URL = 'http://127.0.0.1:8000'

# Get local client
local_client = get_client(url=LOCAL_URL)

# Get curies
curies = local_client.curies()
print(curies)
# Get predicates
predicates = local_client.predicates()
print(predicates)
# Load in queries
with open('simple_queries_1.pk', 'rb') as f_:
    queries = pickle.load(f_)

response = local_client.query(queries[0])
print(json.dumps(response, indent=2))

'''
# Subset queries
TOTAL_QUERIES = 300 #len(queries)
TOTAL_WORKERS = 10
step = TOTAL_QUERIES // TOTAL_WORKERS
subset_queries = []
for i in range(0, TOTAL_QUERIES, step):
    subset_queries.append(queries[i:i+step])
print([len(subset) for subset in subset_queries])

def query_all(queries):
    local_client.query_all(queries)

pool = Pool(TOTAL_WORKERS)
pool.map(query_all, subset_queries)
'''
