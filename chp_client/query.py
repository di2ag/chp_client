"""
Helper module for loading and building CHP queries.
"""

import json
from jsonschema import ValidationError

from chp_client.trapi_constants import *
from chp_client.exceptions import *
from reasoner_validator import validate_QEdge_1_0, validate_QEdge_1_1, \
validate_QNode_1_0, validate_QNode_1_1, validate_Message_1_0, validate_Message_1_1, \
validate_QueryGraph_1_0, validate_QueryGraph_1_1


# Constants
SUBJECT_TO_OBJECT_PREDICATE_MAP = {
        (BIOLINK_GENE, BIOLINK_DRUG): BIOLINK_GENE_TO_CHEMICAL_PREDICATE,
        (BIOLINK_DRUG, BIOLINK_GENE): BIOLINK_CHEMICAL_TO_GENE_PREDICATE,
        (BIOLINK_GENE, BIOLINK_DISEASE): BIOLINK_GENE_TO_DISEASE_PREDICATE,
        (BIOLINK_DRUG, BIOLINK_DISEASE): BIOLINK_CHEMICAL_TO_DISEASE_OR_PHENOTYPIC_FEATURE_PREDICATE,
        }

class QBaseClass:
    def __init__(self, trapi_version):
        self.trapi_version = trapi_version
    
    def json(self, filename=None):
        if filename is None:
            return json.dumps(self.to_dict())
        else:
            with open(filename, 'w') as json_file:
                json.dump(self.to_dict(), json_file)

    def __str__(self):
        return json.dumps(self.to_dict())

class QConstraintOrAdditionalProperty(QBaseClass):
    def __init__(self,
            trapi_version,
            name,
            c_id,
            operator,
            value,
            unit_id=None,
            unit_name=None,
            c_not=False,
            ):
        self.name = name
        self.id = c_id
        self.operator = operator
        self.value = value
        self.unit_id = unit_id
        self.unit_name = unit_name
        super().__init__(trapi_version)

    def to_dict(self):
        if self.trapi_version == '1.0':
            return {
                    self.name: {
                        "id": self.id,
                        "operator": self.operator,
                        "value": self.value,
                        "unit_id": self.unit_id,
                        "unit_name": self.unit_name
                        }
                    }
        elif self.trapi_version == '1.1':
            return {
                        "name": self.name,
                        "id": self.id,
                        "operator": self.operator,
                        "value": self.value,
                        "unit_id": self.unit_id,
                        "unit_name": self.unit_name
                    }
        else:
            raise UnsupportedTrapiVersion(self.trapi_version)


class QNode(QBaseClass):
    def __init__(self,
            trapi_version,
            ids = None,
            categories = None,
            constraints = None,
            ):
        self.ids = ids
        self.categories = categories
        self.constraints = constraints
        super().__init__(trapi_version)

        valid, message = self.validate()
        if not valid:
            raise InvalidTrapiComponent(trapi_version, 'QNode', message)

    def to_dict(self):
        if self.trapi_version == '1.0':
            _dict = {
                        "id": self.ids,
                        "category": self.categories,
                    }
            if self.constraints is not None:
                for constraint in self.constraints:
                    _dict.update(constraint.to_dict())
            return _dict
        elif self.trapi_version == '1.1':
            ids = self.ids
            categories = self.categories
            if type(ids) is not list and ids is not None:
                ids = [ids]
            if type(categories) is not list and categories is not None:
                    categories = [categories]
            _dict = {
                        "ids": ids,
                        "categories": categories,
                        "constraints": []
                    }
            if self.constraints is not None:
                for constraint in self.constraints:
                    _dict["constraints"].append(constraint.to_dict())
            return _dict
        else:
            raise UnsupportedTrapiVersion(self.trapi_version)

    def add_constraint(self, 
            name,
            c_id,
            operator,
            value,
            unit_id=None,
            unit_name=None,
            c_not=False,
            edge_id=None,
            node_id=None,
            ):
        if self.constraints is None:
            self.constraints = []
        self.constraints.append(
                QConstraintOrAdditionalProperty(
                    trapi_version=self.trapi_version,
                    name=name,
                    c_id=c_id,
                    operator=operator,
                    value=value,
                    unit_id=unit_id,
                    unit_name=unit_name,
                    c_not=c_not,
                    )
                )
        valid, message = self.validate()
        if not valid:
            raise InvalidTrapiComponent(trapi_version, 'QNode', message)

    def validate(self):
        _dict = self.to_dict()
        try:
            if self.trapi_version == '1.0':
                validate_QNode_1_0(_dict)
            elif self.trapi_version == '1.1':
                validate_QNode_1_1(_dict)
            else:
                raise UnsupportedTrapiVersion(self.trapi_version)
            return True, None 
        except ValidationError as ex:
                return False, ex.message

class QEdge(QBaseClass):
    def __init__(self,
            trapi_version,
            q_subject,
            q_object,
            predicates=None,
            relation=None,
            constraints=None,
            ):
        self.subject = q_subject
        self.object = q_object
        self.predicates = predicates
        self.relation = relation
        self.constraints = constraints
        super().__init__(trapi_version)
        
        valid, message = self.validate()
        if not valid:
            raise InvalidTrapiComponent(trapi_version, 'QEdge', message)

    def to_dict(self):
        if self.trapi_version == '1.0':
            _dict = {
                    "predicate": self.predicates,
                    "relation": self.relation,
                    "subject": self.subject,
                    "object": self.object,
                    }
            if self.constraints is not None:
                for constraint in self.constraints:
                    _dict.update(constraint.to_dict())
            return _dict
        elif self.trapi_version == '1.1':
            predicates = self.predicates
            if type(predicates) is not list:
                predicates = [predicates]
            _dict = {
                    "predicates": predicates,
                    "relation": self.relation,
                    "subject": self.subject,
                    "object": self.object,
                    }
            if self.constraints is not None:
                _dict["constraints"] = []
                for constraint in self.constraints:
                    _dict["constraints"].append(constraint.to_dict())
            return _dict
    
    def add_constraint(self, 
            name,
            c_id,
            operator,
            value,
            unit_id=None,
            unit_name=None,
            c_not=False,
            edge_id=None,
            node_id=None,
            ):
        if self.constraints is None:
            self.constraints = []
        self.constraints.append(
                QConstraintOrAdditionalProperty(
                    trapi_version=self.trapi_version,
                    name=name,
                    c_id=c_id,
                    operator=operator,
                    value=value,
                    unit_id=unit_id,
                    unit_name=unit_name,
                    c_not=c_not,
                    )
                )
        valid, message = self.validate()
        if not valid:
            raise InvalidTrapiComponent(self.trapi_version, 'QEdge', message)
        
    def validate(self):
        _dict = self.to_dict()
        try:
            if self.trapi_version == '1.0':
                validate_QEdge_1_0(_dict)
            elif self.trapi_version == '1.1':
                validate_QEdge_1_1(_dict)
            else:
                raise UnsuppoertedTrapiVersion(self.trapi_version)
            return True, None 
        except ValidationError as ex:
                return False, ex.message

class Query(QBaseClass):
    def __init__(self, trapi_version='1.1'):
        self.nodes = {}
        self.edges = {}
        self.node_counter = 0
        self.edge_counter = 0
        super().__init__(trapi_version)

    def add_node(self, ids, categories):
        node_id = 'n{}'.format(self.node_counter)
        self.node_counter += 1
        self.nodes[node_id] = QNode(
                trapi_version=self.trapi_version,
                ids=ids,
                categories=categories
                )
        return node_id

    def add_edge(self, q_subject, q_object, predicates, relation=None):
        edge_id = 'e{}'.format(self.edge_counter)
        self.edge_counter += 1
        self.edges[edge_id] = QEdge(
                trapi_version=self.trapi_version,
                q_subject=q_subject,
                q_object=q_object,
                predicates=predicates,
                relation=relation,
                )
        return edge_id

    def add_constraint(self,
            name,
            c_id,
            operator,
            value,
            unit_id=None,
            unit_name=None,
            c_not=False,
            edge_id=None,
            node_id=None,
            ):
        if edge_id is None and node_id is None:
            raise ValueError('Must specify either node or edge id.')
        elif edge_id is not None and node_id is not None:
            raise ValueError('Must specify either node or edge id, not both.')
        if edge_id is not None:
            q_obj = self.edges[edge_id]
        else:
            q_obj = self.nodes[node_id]
        q_obj.add_constraint(
                name,
                c_id,
                operator,
                value,
                unit_id=None,
                unit_name=None,
                c_not=False,
                )
        return True

    def to_dict(self):
        nodes = {}
        edges = {}
        for node_id, node in self.nodes.items():
            nodes[node_id] = node.to_dict()
        for edge_id, edge in self.edges.items():
            edges[edge_id] = edge.to_dict()
        return {
                "nodes": nodes,
                "edges": edges,
                }

    def find_nodes(self, categories=None, ids=None):
        matched_node_ids = []
        for node_id, node_info in self.nodes.items():
            if categories is not None:
                if node_info.categories != categories:
                    continue
            if ids is not None:
                if node_info.ids != ids:
                    continue
            matched_node_ids.append(node_id)
        return matched_node_ids

    def make_trapi_message(self, to_json=False):
        trapi_message = {
                "query_graph": self.to_dict(),
                "knowledge_graph": None,
                "results": None
                }
        if to_json:
            return json.dumps(trapi_message)
        return trapi_message

    def validate_query_graph(self):
        _dict = self.to_dict()
        try:
            if self.trapi_version == '1.0':
                validate_QueryGraph_1_0(_dict)
            elif self.trapi_version == '1.1':
                validate_QueryGraph_1_1(_dict)
            else:
                raise UnsuppoertedTrapiVersion(self.trapi_version)
            return True, None 
        except ValidationError as ex:
            return False, ex.message

    def validate(self):
        _dict = self.make_trapi_message()
        try:
            if self.trapi_version == '1.0':
                validate_Message_1_0(_dict)
            elif self.trapi_version == '1.1':
                validate_Message_1_1(_dict)
            else:
                raise UnsuppoertedTrapiVersion(self.trapi_version)
            return True, None 
        except ValidationError as ex:
            return False, ex.message

def build_standard_query(
        genes=None,
        drugs=None,
        outcome=None,
        outcome_name=None,
        outcome_op=None,
        outcome_value=None,
        disease=None,
        trapi_version='1.1',
        ):

    if genes is None and drugs is None:
        raise QueryBuildError("Both genes and drugs can't be None.")
    if outcome is None:
        raise QueryBuildError('You must specify an outcome CURIE.')
    if outcome_op is None:
        raise QueryBuildError("You must specify an outcome operation consistent with \
                with your desired TRAPI version's Constraint Object.")
    if outcome_value is None:
        raise QueryBuildError('You must specify an outcome value to test.')
    if disease is None:
        raise QueryBuildError('You must specify a disease.')

    # Initialize Query
    q = Query(trapi_version=trapi_version)
    
    # Add disease node
    disease_node = q.add_node(disease, BIOLINK_DISEASE)

    if genes is not None:
        # Add gene nodes
        gene_nodes = []
        for gene in genes:
            gene_nodes.append(q.add_node(gene, BIOLINK_GENE))
    
        # Connect all gene nodes to disease.
        for gene_node in gene_nodes:
            q.add_edge(gene_node, disease_node, BIOLINK_GENE_TO_DISEASE_PREDICATE)

    if drugs is not None:
        # Add drug nodes
        if drugs is not None:
            drug_nodes = []
            for drug in drugs:
                drug_nodes.append(q.add_node(drug, BIOLINK_DRUG))

        # Connect all drug nodes to disease.
        for drug_node in drug_nodes:
            q.add_edge(drug_node, disease_node, BIOLINK_CHEMICAL_TO_DISEASE_OR_PHENOTYPIC_FEATURE_PREDICATE)

    # Connect drug node to outcome node
    outcome_node = q.add_node(outcome, BIOLINK_PHENOTYPIC_FEATURE)
    q.add_constraint(outcome_name, outcome, outcome_op, outcome_value, node_id=outcome_node)
    q.add_edge(disease_node, outcome_node, BIOLINK_DISEASE_TO_PHENOTYPIC_FEATURE_PREDICATE)

    return q


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
        ):

    if wildcard_category is None:
        QueryBuildError('Wildcard category can not be None.')

    
    # Build standard query
    q = build_standard_query(genes, drugs, outcome, outcome_name, outcome_op, outcome_value, disease, trapi_version=trapi_version)
    disease_node = q.find_nodes(categories=BIOLINK_DISEASE)[0]

    wildcard_node = q.add_node(None, wildcard_category)
    # Add wildcard to query
    if wildcard_category == BIOLINK_GENE:
        q.add_edge(wildcard_node, disease_node, BIOLINK_GENE_TO_DISEASE_PREDICATE)
    elif wildcard_category == BIOLINK_DRUG:
        q.add_edge(wildcard_node, disease_node, BIOLINK_CHEMICAL_TO_DISEASE_OR_PHENOTYPIC_FEATURE_PREDICATE)
    else:
        raise InvalidWildcardCategory(wildcard_category)
    return q

def build_onehop_query(
        q_subject,
        q_subject_category,
        q_object,
        q_object_category,
        genes=None,
        drugs=None,
        outcome=None,
        outcome_name=None,
        outcome_op=None,
        outcome_value=None,
        disease=None,
        trapi_version='1.1',
        ):
    # Initialize query
    q = Query(trapi_version)

    # Add nodes
    subject_node = q.add_node(q_subject, q_subject_category)
    object_node = q.add_node(q_object, q_object_category)

    # Add edge
    try:
        edge_predicate = SUBJECT_TO_OBJECT_PREDICATE_MAP[(q_subject_category, q_object_category)]
    except KeyError:
        raise QueryBuildError('Edge from {} to {} is not supported.'.format(q_subject_category, q_object_category))

    edge_id = q.add_edge(subject_node, object_node, edge_predicate)

    # Add constraints
    if outcome is not None:
        q.add_constraint('predicate_proxy', 'CHP:PredicateProxy', '==', outcome_name, edge_id=edge_id)
        q.add_constraint(outcome_name, outcome, outcome_op, outcome_value, edge_id=edge_id)
    
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
    return q
