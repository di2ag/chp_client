""" Simple script for generating TRAPI query samples.
"""

import json

from chp_client.query import build_query


def make_standard_probablistic_query_one_gene():
    """ Build a standard probablistic query with one gene and one drug.
    """
    query = build_query(
            genes=["ENSEMBL:ENSG00000141510"],
            therapeutic="CHEMBL:CHEMBL88",
            disease="MONDO:0007254",
            outcome=("EFO:0000714", ">=", 500)
            )
    
    with open('standard_one_gene.json', 'w') as f_:
        json.dump(query, f_)    

def make_standard_probablistic_query_two_gene():
    """ Build a standard probablistic query with two genes and one drug.
    """
    query = build_query(
            genes=["ENSEMBL:ENSG00000121879", "ENSEMBL:ENSG00000155657"],
            therapeutic="CHEMBL:CHEMBL88",
            disease="MONDO:0007254",
            outcome=("EFO:0000714", ">=", 500)
            )
    
    with open('standard_two_gene.json', 'w') as f_:
        json.dump(query, f_)    

def make_gene_wildcard_query():
    """ Builds a gene wildcard query
    """
    query = build_query(
            therapeutic="CHEMBL:CHEMBL88",
            disease="MONDO:0007254",
            outcome=("EFO:0000714", ">=", 500),
            num_gene_wildcards=1,
            )

    with open('gene_wildcard.json', 'w') as f_:
        json.dump(query, f_)    

def make_drug_wildcard_query():
    for i in [1,2,5,10]:
        query = build_query(
                genes=["ENSEMBL:ENSG00000012048"],
                disease="MONDO:0007254",
                outcome=("EFO:0000714", ">=", 365*i),
                therapeutic_wildcard=True,
                )

        with open('dw_brac1_{}yr.json'.format(i), 'w') as f_:
            json.dump(query, f_)

def make_one_hop_query():
    query = build_query(
            genes=["ENSEMBL:ENSG00000121879"],
            therapeutic_wildcard=True,
            one_hop=True,
            )

    with open('one_hop.json', 'w') as f_:
        json.dump(query, f_)

def main():
    #make_standard_probablistic_query_one_gene()
    #make_standard_probablistic_query_two_gene()
    #make_gene_wildcard_query()
    make_drug_wildcard_query()
    #make_one_hop_query()

if __name__ == "__main__":
    main()
