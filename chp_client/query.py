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
    # empty response
    message = {
            "query_graph": {},
            "knowledge_graph": {},
            "results": {}
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

    # empty response graph
    message["results"] = {
            "node_bindings": {},
            "edge_bindings": {}
            }

    node_count = 0
    edge_count = 0

    # add genes
    for gene in genes:
        message["query_graph"]["nodes"].append({
                "id": 'n{}'.format(node_count),
                "type":'gene',
                "curie": gene
                })
        node_count += 1

    # add gene wildcards (if applicable)
    for _ in range(num_gene_wildcards):
        message["query_graph"]["nodes"].append({
                "id": 'n{}'.format(node_count),
                "type": 'gene'
                })
        node_count += 1


    # add drugs
    if therapeutic_wildcard:
        raise NotImplementedError('Currently therapeutic wildcards are not supported.')
        #TODO: Add drug wildcards to CHP
        #message["query_graph"]["nodes"].append({
        #        "type": 'chemical_substance',
        #        "id": 'n{}'.format(node_count),
        #        }
        #node_count += 1

    else:
        message["query_graph"]["nodes"].append({
                "id": 'n{}'.format(node_count),
                "type": 'chemical_substance',
                "curie": therapeutic
                })
        node_count += 1

    # add in disease node
    message["query_graph"]["nodes"].append({
            "id": 'n{}'.format(node_count),
            "type": 'disease',
            "curie": disease
            })
    node_count += 1

    # link all evidence to disease
    for node in message["query_graph"]["nodes"]:
        if node["type"] == 'gene':
            message["query_graph"]["edges"].append({
                    "id": 'e{}'.format(edge_count),
                    "type":'gene_to_disease_association',
                    "source_id": node_id,
                    "target_id": 'n{}'.format(node_count - 1)   # should be disease node
                    })
            edge_count += 1
        elif node["type"] == 'chemical_substance':
            message["query_graph"]["edges"].append({
                    "id": 'e{}'.format(edge_count),
                    "type":'chemical_to_disease_or_phenotypic_feature_association',
                    "source_id": node_id,
                    "target_id": 'n{}'.format(node_count -1)  # should be disease node
                    })
            edge_count += 1

    # add target outcome node
    outcome_curie, op, value = outcome
    message["query_graph"]["nodes"].append({
            "id": 'n{}'.format(node_count),
            "type": 'phenotypicfeature',
            "curie": outcome_curie,
            })
    node_count += 1

    # link disease to target
    message["query_graph"]["edges"].append({
            "id": 'e{}'.format(edge_count),
            "type": 'disease_to_phenotype_association',
            "source_id": 'n{}'.format(node_count-2),
            "target_id": 'n{}'.format(node_count-1),
            "properties": {
                    "qualifier": op,
                    "value": value
                    }
            })
    return message


