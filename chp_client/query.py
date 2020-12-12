"""
Helper module for loading and building CHP queries.
"""

import json


def load_query(filename):
    """ Loads a saved JSON query.
    """
    with open(filename, 'r') as f_:
        q = json.load(f_)
    return q

def save_query(q, filename):
    """ Saves a json query.
    """
    with open(filename, 'w') as f_:
        json.dump(q, f_)
    return filename

def build_query(
        genes=None,
        therapeutic=None,
        outcome=None,
        disease=None,
        num_gene_wildcards=0,
        therapeutic_wildcard=False
        ):
    """ Helper function to build CHP JSON queries.

    Args:
        genes: A list of ENSEMBL gene curies (max 10).
        therapeutic: A string CHEMBL curie for a drug/therputic.
        outcome: A patient outcome tuple of the form ({outcome curie}, {numerical inequality}, {float}).
        disease: A MONDO disease curie string.
        num_gene_wildcards: Number of gene wildcards that will be filled by CHP. Default: 0.
        therapeutic_wildcard: Boolean letting CHP know if it should try to find a statistically important therapeutic. Default: False.

    """
    # Initialize
    if genes is None:
        genes = []

    # empty response
    message = {
            "query_graph": {},
            "knowledge_graph": {},
            "results": []
            }
    # empty query graph
    message["query_graph"] = {
            "edges": {},
            "nodes": {}
            }

    # empty knowledge graph
    message["knowledge_graph"] = {
            "edges": {},
            "nodes": {}
            }

    node_count = 0
    edge_count = 0

    # add genes
    for gene in genes:
        message["query_graph"]["nodes"]['n{}'.format(node_count)] = {
                "category":"biolink:Gene",
                "id": gene
                }
        node_count += 1

    # add gene wildcards (if applicable)
    for _ in range(num_gene_wildcards):
        message["query_graph"]["nodes"]['n{}'.format(node_count)] = {
                "category": 'biolink:Gene'
                }
        node_count += 1


    # add drugs
    if therapeutic_wildcard:
        message["query_graph"]["nodes"]['n{}'.format(node_count)] = {
            "category": 'biolink:Drug',
                }
        node_count += 1

    elif therapeutic is not None:
        message["query_graph"]["nodes"]['n{}'.format(node_count)] = {
                "category": 'biolink:Drug',
                "id": therapeutic
                }
        node_count += 1

    # add in disease node
    message["query_graph"]["nodes"]['n{}'.format(node_count)] = {
            "category": 'biolink:Disease',
            "id": disease
            }
    node_count += 1

    # link all evidence to disease
    for node_id, node in message["query_graph"]["nodes"].items():
        if node["category"] == 'biolink:Gene':
            message["query_graph"]["edges"]['e{}'.format(edge_count)] = {
                    "predicate":'biolink:GeneToDiseaseAssociation',
                    "subject": node_id,
                    "object": 'n{}'.format(node_count - 1)   # should be disease node
                    }
            edge_count += 1
        elif node["category"] == 'biolink:Drug':
            message["query_graph"]["edges"]['e{}'.format(edge_count)] = {
                    "predicate":'biolink:ChemicalToDiseaseOrPhenotypicFeatureAssociation',
                    "subject": node_id,
                    "object": 'n{}'.format(node_count -1)  # should be disease node
                    }
            edge_count += 1

    # add target outcome node
    outcome_curie, op, value = outcome
    message["query_graph"]["nodes"]['n{}'.format(node_count)] = {
            "category": 'biolink:PhenotypicFeature',
            "id": outcome_curie,
            }
    node_count += 1

    # link disease to target
    message["query_graph"]["edges"]['e{}'.format(edge_count)] = {
            "predicate": 'biolink:DiseaseToPhenotypicFeatureAssociation',
            "subject": 'n{}'.format(node_count-2),
            "object": 'n{}'.format(node_count-1),
            "properties": {
                           "qualifier": op,
                           "days": value
                          }
            }
    return {"message": message}
