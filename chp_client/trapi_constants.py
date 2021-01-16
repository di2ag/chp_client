import logging
#from chp_client import get_client

# Set up logger
logger = logging.getLogger(__name__)

# Try to pull most up-to-date constants from endpoint.
#try:
#    client = get_client()
#    constants = client.constants()
#    logger.info('Loaded most recent constants from endpoint')
#except:
#    logger.warning('Could not reach constants endpoint, so loading default entities and predicates. May experience compatiability issues.')
constants = {}

# Biolink Entities
BIOLINK_GENE = constants.pop("BIOLINK_GENE", 'biolink:Gene')
BIOLINK_DRUG = constants.pop("BIOLINK_DRUG", 'biolink:Drug')
BIOLINK_DISEASE = constants.pop("BIOLINK_DISEASE", 'biolink:Disease')
BIOLINK_PHENOTYPIC_FEATURE = constants.pop("BIOLINK_PHENOTYPIC_FEATURE", 'biolink:PhenotypicFeature')

# Edge Property Constants
BIOLINK_CONTRIBUTION = constants.pop("BIOLINK_CONTRIBUTION", "biolink:has_evidence")
BIOLINK_PROBABILITY = constants.pop("BIOLINK_PROBABILITY", "biolink:has_confidence_level")

# Biolink Predicate/Association/Slot Constants
BIOLINK_GENE_TO_DISEASE_PREDICATE = constants.pop("BIOLINK_GENE_TO_DISEASE_PREDICATE", 'biolink:affects')
BIOLINK_CHEMICAL_TO_DISEASE_OR_PHENOTYPIC_FEATURE_PREDICATE = constants.pop("BIOLINK_CHEMICAL_TO_DISEASE_OR_PHENOTYPIC_FEATURE_PREDICATE", 'biolink:affects')
BIOLINK_CHEMICAL_TO_GENE_PREDICATE = constants.pop("BIOLINK_CHEMICAL_TO_GENE_PREDICATE", 'biolink:affects')
BIOLINK_DISEASE_TO_PHENOTYPIC_FEATURE_PREDICATE = constants.pop("BIOLINK_DISEASE_TO_PHENOTYPIC_FEATURE_PREDICATE", 'biolink:has_phenotype')
