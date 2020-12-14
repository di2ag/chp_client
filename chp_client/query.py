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

def _build_one_hop(genes, therapeutic, num_gene_wildcards, therapeutic_wildcard):
    if genes is None:
        genes = []
    # Error Handling
    if len(genes) > 0:
        if num_gene_wildcards > 0:
            raise ValueError('Can not specify both a gene and a gene wildcard at the same time.')
        if not therapeutic_wildcard:
            raise ValueError('If you specify a gene than you must specify a therapeutic wildcard.')
        if therapeutic is not None:
            raise ValueError('If you specify a gene than you must specify a therapeutic wildcard.')
    else:
        if num_gene_wildcards == 0:
            raise ValueError('You need to specify either a gene or a gene wildcard.')
        if therapeutic_wildcard:
            raise ValueError('If you specify a gene wildcard than you CAN NOT use therapeutic wildcard.')
        if therapeutic is None:
            raise ValueError('If you specify a gene wildcard than you CAN NOT use therapeutic wildcard.')
    # Build the query
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

    if node_count != 2:
        raise ValueError('Malformed one hop query: Number of nodes are not 2. Check your inputs.')

    # Link two nodes together
    if num_gene_wildcards > 0 or len(genes) == 0:
        # This is a gene wildcard query
        for node_id, node in message["query_graph"]["nodes"].items():
            if node["category"] == 'biolink:Gene':
                # Get object node
                obj_node_id = list(set(message["query_graph"]["nodes"]) - {node_id})[0]
                message["query_graph"]["edges"]['e{}'.format(edge_count)] = {
                        "predicate":'biolink:GeneToChemicalAssociation',
                        "subject": node_id,
                        "object": obj_node_id
                        }
                edge_count += 1

    elif therapeutic is None or therapeutic_wildcard:
        # This is a gene wildcard query
        for node_id, node in message["query_graph"]["nodes"].items():
            if node["category"] == 'biolink:Drug':
                # Get object node
                obj_node_id = list(set(message["query_graph"]["nodes"]) - {node_id})[0]
                message["query_graph"]["edges"]['e{}'.format(edge_count)] = {
                        "predicate":'biolink:ChemicalToGeneAssociation',
                        "subject": node_id,
                        "object": obj_node_id
                        }
                edge_count += 1

    if edge_count != 1:
        raise ValueError('Malformed query: Edge count was not equal to 1. Check your inputs.')

    return {"message": message}

def build_query(
        genes=None,
        therapeutic=None,
        outcome=None,
        disease=None,
        num_gene_wildcards=0,
        therapeutic_wildcard=False,
        one_hop=False
        ):
    """ Helper function to build CHP JSON queries.

    Args:
        genes: A list of ENSEMBL gene curies (max 10).
        therapeutic: A string CHEMBL curie for a drug/therputic.
        outcome: A patient outcome tuple of the form ({outcome curie}, {numerical inequality}, {float}).
        disease: A MONDO disease curie string.
        num_gene_wildcards: Number of gene wildcards that will be filled by CHP. Default: 0.
        therapeutic_wildcard: Boolean letting CHP know if it should try to find a statistically important therapeutic. Default: False.
        one_hop: A boolean that lets you build a one hop query (i.e. 2 nodes one edge) between either a gene/drug wildcard and a gene/drug
            non wildcard. Uses a default surival time of >= 970 and disease is assumed to be breast cancer.
    """
    if one_hop:
        return _build_one_hop(genes, therapeutic, num_gene_wildcards, therapeutic_wildcard)
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
