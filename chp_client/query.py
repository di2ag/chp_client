"""
Helper module for loading and building CHP queries.
"""

import json
from jsonschema import ValidationError

from trapi_model.query import Query
from trapi_model.message import Message
from trapi_model.biolink.constants import *

from chp_client.exceptions import *

OBJECT_TO_SUBJECT_PREDICATE_MAP = {
        BIOLINK_GENE: {
            BIOLINK_DRUG: BIOLINK_INTERACTS_WITH,
            BIOLINK_DISEASE: BIOLINK_GENE_ASSOCIATED_WITH_CONDITION,
            },
        BIOLINK_DRUG: {
            BIOLINK_GENE: BIOLINK_INTERACTS_WITH,
            BIOLINK_DISEASE: BIOLINK_TREATS,
            }
        }

def build_standard_query(
        genes=None,
        drugs=None,
        outcome=None,
        outcome_name=None,
        outcome_op=None,
        outcome_value=None,
        disease=None,
        trapi_version='1.1',
        biolink_version=None,
        batch_genes=None,
        batch_drugs=None,
        batch_diseases=None,
        ):

    if outcome is None:
        raise QueryBuildError('You must specify an outcome CURIE.')
    if outcome_op is None:
        raise QueryBuildError("You must specify an outcome operation consistent with \
                with your desired TRAPI version's Constraint Object.")
    if outcome_value is None:
        raise QueryBuildError('You must specify an outcome value to test.')
    if disease is None and batch_diseases is None:
        raise QueryBuildError('You must specify a disease.')
    if disease is not None and batch_diseases is not None:
        raise QueryBuildError('Only specify either diseases or batch diseases not both.')

    # Initialize Message
    message = Message(trapi_version, biolink_version)
    q = message.query_graph
    
    # Add disease or batch disease node
    if disease is not None:
        disease_node = q.add_node(disease, BIOLINK_DISEASE)
    else:
        disease_node = q.add_node(batch_diseases, BIOLINK_DISEASE)

    if genes is not None:
        # Add gene nodes
        gene_nodes = []
        for gene in genes:
            gene_nodes.append(q.add_node(gene, BIOLINK_GENE))
    
        # Connect all gene nodes to disease.
        for gene_node in gene_nodes:
            q.add_edge(gene_node, disease_node, BIOLINK_GENE_ASSOCIATED_WITH_CONDITION)

    # Setup batch genes
    if batch_genes is not None:
        if type(batch_genes) is not list:
            raise QueryBuildError('Batch genes must be a list.')
        batch_gene_node = q.add_node(batch_genes, BIOLINK_GENE)
        q.add_edge(batch_gene_node, disease_node, BIOLINK_GENE_ASSOCIATED_WITH_CONDITION)

    if drugs is not None:
        # Add drug nodes
        if drugs is not None:
            drug_nodes = []
            for drug in drugs:
                drug_nodes.append(q.add_node(drug, BIOLINK_DRUG))

        # Connect all drug nodes to disease.
        for drug_node in drug_nodes:
            q.add_edge(drug_node, disease_node, BIOLINK_TREATS)

    # Setup batch drugs
    if batch_drugs is not None:
        if type(batch_drugs) is not list:
            raise QueryBuildError('Batch drugs must be a list.')
        batch_drug_node = q.add_node(batch_drugs, BIOLINK_DRUG)
        q.add_edge(batch_drug_node, disease_node, BIOLINK_TREATS)

    # Connect drug node to outcome node
    outcome_node = q.add_node(outcome, BIOLINK_PHENOTYPIC_FEATURE)
    phenotype_edge = q.add_edge(disease_node, outcome_node, BIOLINK_HAS_PHENOTYPE)
    q.add_constraint(outcome_name, outcome, outcome_op, outcome_value, edge_id=phenotype_edge)

    query = Query(trapi_version=trapi_version, biolink_version=biolink_version)
    query.message = message
    return query


def build_wildcard_query(
        wildcard_category=None,
        genes=None,
        drugs=None,
        outcome=None,
        outcome_name=None,
        outcome_op=None,
        outcome_value=None,
        disease=None,
        trapi_version='1.1',
        biolink_version=None,
        batch_genes=None,
        batch_drugs=None,
        batch_diseases=None,
        ):

    if wildcard_category is None:
        QueryBuildError('Wildcard category can not be None.')

    
    # Build standard query
    query = build_standard_query(
            genes, 
            drugs,
            outcome,
            outcome_name,
            outcome_op,
            outcome_value,
            disease,
            trapi_version=trapi_version,
            biolink_version=biolink_version,
            batch_genes=batch_genes,
            batch_drugs=batch_drugs,
            batch_diseases=batch_diseases,
            )
    q = query.message.query_graph
    disease_node = q.find_nodes(categories=BIOLINK_DISEASE_ENTITY)[0]

    wildcard_node = q.add_node(None, wildcard_category)
    # Add wildcard to query
    if wildcard_category == BIOLINK_GENE:
        q.add_edge(wildcard_node, disease_node, BIOLINK_GENE_ASSOCIATED_WITH_CONDITION)
    elif wildcard_category == BIOLINK_DRUG:
        q.add_edge(wildcard_node, disease_node, BIOLINK_TREATS)
    else:
        raise InvalidWildcardCategory(wildcard_category)
    return query

def build_onehop_query(
        q_object_category,
        q_subject_category,
        q_subject=None,
        q_object=None,
        genes=None,
        drugs=None,
        outcome=None,
        outcome_name=None,
        outcome_op=None,
        outcome_value=None,
        disease=None,
        trapi_version='1.1',
        biolink_version=None,
        ):
    # Initialize query
    message = Message(trapi_version, biolink_version)
    q = message.query_graph

    # Add nodes
    subject_node = q.add_node(q_subject, q_subject_category)
    object_node = q.add_node(q_object, q_object_category)

    # Add edge
    try:
        edge_predicate = OBJECT_TO_SUBJECT_PREDICATE_MAP[q_object_category][q_subject_category]
    except KeyError:
        raise QueryBuildError('Edge from {} to {} is not supported.'.format(q_subject_category, q_object_category))

    edge_id = q.add_edge(subject_node, object_node, edge_predicate)

    # Add constraints
    if outcome is not None:
        q.add_constraint('predicate_proxy', 'CHP:PredicateProxy', '==', [outcome], edge_id=edge_id)
        q.add_constraint(outcome, outcome, outcome_op, outcome_value, edge_id=edge_id)
    
    # Get context
    context = []
    if genes is not None:
        context.append(BIOLINK_GENE)
    if drugs is not None:
        context.append(BIOLINK_DRUG)
    if disease is not None:
        context.append(BIOLINK_DISEASE)

    # Process context
    if len(context) > 0:
        q.add_constraint('predicate_context', 'CHP:PredicateContext', '==', context, edge_id=edge_id)
        if genes is not None:
            q.add_constraint(BIOLINK_GENE, BIOLINK_GENE, 'matches', genes, edge_id=edge_id)
        if drugs is not None:
            q.add_constraint(BIOLINK_DRUG, BIOLINK_DRUG, 'matches', drugs, edge_id=edge_id)
        if disease is not None:
            q.add_constraint(BIOLINK_DISEASE, BIOLINK_DISEASE, 'matches', disease, edge_id=edge_id)
    query = Query(trapi_version=trapi_version, biolink_version=biolink_version)
    query.message = message
    return query
