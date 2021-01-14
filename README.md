# Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
  - [Optional libraries](#optional-libraries)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Building Supported Queries](#building-supported-chp-queries)
  - [Standard Queries](#standard-probablistic-query-one-query-one-result)
    - [Single Gene Queries](#single-gene-queries)
    - [Multiple Gene Queries](#multi-gene-queries)
  - [Gene Wildcard Queries](#gene-wildcard-query-one-query-many-results)
  - [Drug Wildcard Queries](#drug-wildcard-query-one-query-many-results)
- [CHP Query Semantics](#chp-query-semantics)
- [API Documentation](#api-documentation)

# Introduction
The *chp_client* is a lightweight Python client for the NCATS Connections Hypothesis Provider (CHP). It is meant to be an easy-to-use wrapper utility to both run and build TRAPI queries the CHP web service will understand. Many of the CHP queries have been inspired by direct input from Translator ARAs and such ARAs may have their own dedicated CHP API client that returns results that they expect. However, there is also a default client that can handle generic CHP requests. 

# Requirements
  - Python >= 3.6
  - [requests](https://pypi.python.org/pypi/requests)
  
## Optional libraries
  - [requests_cache](https://pypi.python.org/pypi/requests-cache) *(Allows user to setup of requests caching.)*

# Installation
## Option 1
``` python3 setup.py install ```
## Option 2
```pip3 install -e git+https://github.com/di2ag/chp_client#egg=chp_client```

# Quick Start
Once you have installed the CHP client, useage is as simple as:
``` python3
In [1]: from chp_client import get_client

In [2]: default_client = get_client()
```

Now that you have an instance of the client, you can determine which query graph edge predicates are currently supported by CHP with:

```python3
In[3]: default_client.predicates()
{
  "biolink:Drug": {
    "biolink:Gene": [
      "biolink:ChemicalToGeneAssociation"
    ],
    "biolink:Disease": [
      "biolink:ChemicalToDiseaseOrPhenotypicFeatureAssociation"
    ]
  },
  "biolink:Disease": {
    "biolink:PhenotypicFeature": [
      "biolink:DiseaseToPhenotypicFeatureAssociation"
    ]
  },
  "biolink:Gene": {
    "biolink:Disease": [
      "biolink:GeneToDiseaseAssociation"
    ]
  }
}
```

And you can check the supported curies by:

```python3
In [4]: default_client.curies()
{
  "biolink:Drug": [
    {
      "name": "ZOLADEX",
      "id": "CHEMBL:CHEMBL1201247"
    },
    {
      "name": "CYCLOPHOSPHAMIDE",
      "id": "CHEMBL:CHEMBL88"
    }, ...
  ]
  "biolink:PhenotypicFeature": [
    {
      "name": "survival_time",
      "id": "EFO:0000714"
    }
  ],
  "biolink:Disease": [
    {
      "name": "breast_cancer",
      "id": "MONDO:0007254"
    }
  ],
  "biolink:Gene": [
    {
      "name": "CLIP2",
      "id": "ENSEMBL:ENSG00000106665"
    },
    {
      "name": "PI4KA",
      "id": "ENSEMBL:ENSG00000241973"
    },
    {
      "name": "CELSR2",
      "id": "ENSEMBL:ENSG00000143126"
    }, ...
  ]
}
```
This function will return a dictionary of supported biolink entities (NamedThings) that are supported by CHP along with a list of curies for each type. The list will include both our internal CHP name for the entity along with its associated curie for better human readability. *Note: When building query graphs only specify the appropriate curie. There is no need to also specify our internal name that we provide.*

Now that we know which curies and predicates are supported by CHP we can post a query to CHP via:

```python3
In [5]: default_client.query(q)
```
In the next section we will look at how to build CHP queries.

# Building Supported CHP Queries
As CHP is TRAPI compliant a large subset of queries can be built with a wide variety of structures. In order to scope the query building problem, we have currently limited the structures of queries that can be asked and have detailed their respective semantics. *Note: As the Translator and Biolink models develop we intend to ease these restrictions.*

## Standard Probablistic Query (One query, one result)
### Single Gene Queries
Our standard query is a straight probabilistic query of the form *P(Outcome | Gene Mutations, Disease, Therapeutics, ...)*. We can see a graphical representation of a query below:

<img src="media/qg-oneGene_oneDrug.png" width=600>

Notice, that the CHP is inherently a multi-hop knowledge provider. We reason in the full contents of the query graph and return the appropriate response. In this case the respose will be a edge binding to the disease_to_phenotypic_feature_association in this query graph. Where the resultant calculated knowledge graph of this query graph will have a *has_confidence* attribute denoting the calculated probability for this query. We can build this query with the provided query module of the client with the following code:

```python
In [6]: from chp_client.query import build_query

In [7]: q = build_query(
   ...: genes=['ENSEMBL:ENSG00000141510'],
   ...: therapeutic='CHEMBL:CHEMBL1201585',
   ...: disease='MONDO:0007254',
   ...: outcome=('EFO:0000714', '>=', 500)
   )
   
In [8]: response = client.query(q)
```

An example response from this type of query graph is below:

```json
{
  "message": {
    "query_graph": {
      "edges": {
        "e0": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "n0",
          "object": "n2"
        },
        "e1": {
          "predicate": "biolink:ChemicalToDiseaseOrPhenotypicFeatureAssociation",
          "subject": "n1",
          "object": "n2"
        },
        "e2": {
          "predicate": "biolink:DiseaseToPhenotypicFeatureAssociation",
          "subject": "n2",
          "object": "n3",
          "properties": {
            "qualifier": ">=",
            "days": 500
          }
        }
      },
      "nodes": {
        "n0": {
          "category": "biolink:Gene",
          "id": "ENSEMBL:ENSG00000141510"
        },
        "n1": {
          "category": "biolink:Drug",
          "id": "CHEMBL:CHEMBL1201585"
        },
        "n2": {
          "category": "biolink:Disease",
          "id": "MONDO:0007254"
        },
        "n3": {
          "category": "biolink:PhenotypicFeature",
          "id": "EFO:0000714"
        }
      }
    },
    "knowledge_graph": {
      "edges": {
        "kge0": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "ENSEMBL:ENSG00000141510",
          "object": "MONDO:0007254"
        },
        "kge1": {
          "predicate": "biolink:ChemicalToDiseaseOrPhenotypicFeatureAssociation",
          "subject": "CHEMBL:CHEMBL1201585",
          "object": "MONDO:0007254"
        },
        "kge2": {
          "predicate": "biolink:DiseaseToPhenotypicFeatureAssociation",
          "subject": "MONDO:0007254",
          "object": "EFO:0000714",
          "properties": {
            "qualifier": ">=",
            "days": 500
          },
          "has_confidence_level": 0.8499999999999999
        }
      },
      "nodes": {
        "ENSEMBL:ENSG00000132155": {
          "category": "biolink:Gene",
          "name": "TP53"
        },
        "CHEMBL:CHEMBL1201585": {
          "category": "biolink:Drug",
          "name": "TRASTUZUMAB"
        },
        "MONDO:0007254": {
          "category": "biolink:Disease"
        },
        "EFO:0000714": {
          "category": "biolink:PhenotypicFeature"
        }
      }
    },
    "results": [
      {
        "edge_bindings": {
          "e0": [
            {
              "id": "kge0"
            }
          ],
          "e1": [
            {
              "id": "kge1"
            }
          ],
          "e2": [
            {
              "id": "kge2"
            }
          ]
        },
        "node_bindings": {
          "n0": [
            {
              "id": "ENSEMBL:ENSG00000141510"
            }
          ],
          "n1": [
            {
              "id": "CHEMBL:CHEMBL1201585"
            }
          ],
          "n2": [
            {
              "id": "MONDO:0007254"
            }
          ],
          "n3": [
            {
              "id": "EFO:0000714"
            }
          ]
        }
      }
    ]
  }
}

```

#### Extracting Query Probability
You can extract the probability of the query manually from the TRAPI response data from CHP, but we have also provided a helper method inside the client to assist in extracting this probability.

```python
In [9]: client.get_outcome_prob(response)
Out[9]: 0.8499999999999999
```

The interpretation of this probability is that all patients in our dataset with a somatic mutation in RAF1 gene that took herceptin survived for more than 500 days after initial diagnosis.

### Multi-Gene Queries
As the CHP is inherenly multi-hop, we can easily add multiple genes to our query graph and calcuate the probability of a patient outcome in the presence of multiple gene mutations. A sample query graph is below *(We have not graphed the edge labels for ease of view but they are there in the query graph)*:

<img src="media/qg-manyGenes_oneDrug.png" width=600>

A result from the CHP will again be a single edge binding as in the single gene case with the associated probability of the query in the *has_confidence_level* attribute. We can also use our *build_query* function instead the CHP client's query module to build a Multi-Gene query. Example code for building the above query is:

```python
In [10]: q = build_query(
   ...: genes=['ENSEMBL:ENSG00000132155', 'ENSEMBL:ENSG00000196557', 'ENSEMBL:ENSG00000141510'],
   ...: therapeutic='CHEMBL:CHEMBL1201585',
   ...: disease='MONDO:0007254',
   ...: outcome=('EFO:0000714', '>=', 2000)
   )
   
In [11]: response = client.query(q)
```

A sample json response from this multi-gene query is below:

```json
"message": {
    "query_graph": {
      "edges": {
        "e0": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "n0",
          "object": "n4"
        },
        "e1": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "n1",
          "object": "n4"
        },
        "e2": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "n2",
          "object": "n4"
        },
        "e3": {
          "predicate": "biolink:ChemicalToDiseaseOrPhenotypicFeatureAssociation",
          "subject": "n3",
          "object": "n4"
        },
        "e4": {
          "predicate": "biolink:DiseaseToPhenotypicFeatureAssociation",
          "subject": "n4",
          "object": "n5",
          "properties": {
            "qualifier": ">=",
            "days": 500
          }
        }
      },
      "nodes": {
        "n0": {
          "category": "biolink:Gene",
          "id": "ENSEMBL:ENSG00000132155"
        },
        "n1": {
          "category": "biolink:Gene",
          "id": "ENSEMBL:ENSG00000196557"
        },
        "n2": {
          "category": "biolink:Gene",
          "id": "ENSEMBL:ENSG00000196557"
        },
        "n3": {
          "category": "biolink:Drug",
          "id": "CHEMBL:CHEMBL1201585"
        },
        "n4": {
          "category": "biolink:Disease",
          "id": "MONDO:0007254"
        },
        "n5": {
          "category": "biolink:PhenotypicFeature",
          "id": "EFO:0000714"
        }
      }
    },
    "knowledge_graph": {
      "edges": {
        "kge0": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "ENSEMBL:ENSG00000132155",
          "object": "MONDO:0007254"
        },
        "kge1": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "ENSEMBL:ENSG00000196557",
          "object": "MONDO:0007254"
        },
        "kge2": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "ENSEMBL:ENSG00000196557",
          "object": "MONDO:0007254"
        },
        "kge3": {
          "predicate": "biolink:ChemicalToDiseaseOrPhenotypicFeatureAssociation",
          "subject": "CHEMBL:CHEMBL1201585",
          "object": "MONDO:0007254"
        },
        "kge4": {
          "predicate": "biolink:DiseaseToPhenotypicFeatureAssociation",
          "subject": "MONDO:0007254",
          "object": "EFO:0000714",
          "properties": {
            "qualifier": ">=",
            "days": 500
          },
          "has_confidence_level": -1
        }
      },
      "nodes": {
        "ENSEMBL:ENSG00000132155": {
          "category": "biolink:Gene",
          "name": "RAF1"
        },
        "ENSEMBL:ENSG00000196557": {
          "category": "biolink:Gene",
          "name": "CACNA1H"
        },
        "CHEMBL:CHEMBL1201585": {
          "category": "biolink:Drug",
          "name": "TRASTUZUMAB"
        },
        "MONDO:0007254": {
          "category": "biolink:Disease"
        },
        "EFO:0000714": {
          "category": "biolink:PhenotypicFeature"
        }
      }
    },
    "results": [
      {
        "edge_bindings": {
          "e0": [
            {
              "id": "kge0"
            }
          ],
          "e1": [
            {
              "id": "kge1"
            }
          ],
          "e2": [
            {
              "id": "kge2"
            }
          ],
          "e3": [
            {
              "id": "kge3"
            }
          ],
          "e4": [
            {
              "id": "kge4"
            }
          ]
        },
        "node_bindings": {
          "n0": [
            {
              "id": "ENSEMBL:ENSG00000132155"
            }
          ],
          "n1": [
            {
              "id": "ENSEMBL:ENSG00000196557"
            }
          ],
          "n2": [
            {
              "id": "ENSEMBL:ENSG00000196557"
            }
          ],
          "n3": [
            {
              "id": "CHEMBL:CHEMBL1201585"
            }
          ],
          "n4": [
            {
              "id": "MONDO:0007254"
            }
          ],
          "n5": [
            {
              "id": "EFO:0000714"
            }
          ]
        }
      }
    ]
  }
}
```

#### Extracting Query Probability
You can extract the probability of the query manually from the TRAPI response data from CHP the same way as for a single gene query, as well as using the *get_outcome_prob* function as we did in the single gene query.

```python
In [12]: client.get_outcome_prob(response)
Out[12]: -1
```

**Interpreting a -1 probability result:** A -1 query probability is not an error and should not be treated as simply zero. What this value actually means is that CHP was not able to find an inference that supported all the gene and therauptic evidence with the given outcome condition. This is an inherent artifact of probabilistic incompleteness. The interpretation should instead be that there is insufficient information in our dataset/model to provide an answer to the query.

## Gene Wildcard Query (One query, many results)
CHP also has the capability to statistically rank genes based on their overall importance to a query. We call these *Gene Wildcard* queries, as the goal is to fill in the most statistically important gene into the wildcard placeholder node. A sample query graph is located below:

<img src="media/qg-geneWildcard.png" width=600>

In this query the CHP will calculate the standard probabilistic query of the subgraph not including the gene wildcard, i.e. *P(outcome | therapuetic, disease, etc)*. We can also use the *build_query* function in the CHP client query module to build a gene wildcard query.

```python
In [13]: q = build_query(
    ...: therapeutic='CHEMBL:CHEMBL1201585',
    ...: disease='MONDO:0007254',
    ...: outcome=('EFO:0000714', '>=', 500),
    ...: num_gene_wildcards=1
    )

ln [14]: client.query(q)
```

The sample json response from this query is:

```json
{
  "message": {
    "query_graph": {
      "edges": {
        "e0": {
          "predicate": "biolink:DiseaseToPhenotypicFeatureAssociation",
          "subject": "n2",
          "object": "n3",
          "properties": {
            "qualifier": ">=",
            "days": 500
          }
        },
        "e1": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "n1",
          "object": "n2"
        },
        "e2": {
          "predicate": "biolink:ChemicalToDiseaseOrPhenotypicFeatureAssociation",
          "subject": "n0",
          "object": "n2"
        }
      },
      "nodes": {
        "n0": {
          "category": "biolink:Drug",
          "id": "CHEMBL:CHEMBL1201585"
        },
        "n1": {
          "category": "biolink:Gene"
        },
        "n2": {
          "category": "biolink:Disease",
          "id": "MONDO:0007254"
        },
        "n3": {
          "category": "biolink:PhenotypicFeature",
          "id": "EFO:0000714"
        }
      }
    },
    "knowledge_graph": {
      "edges": {
        "kge0": {
          "predicate": "biolink:DiseaseToPhenotypicFeatureAssociation",
          "subject": "MONDO:0007254",
          "object": "EFO:0000714",
          "properties": {
            "qualifier": ">=",
            "days": 500
          },
          "has_confidence_level": 0.8412698412698413
        },
        "kge1": {
          "predicate": "biolink:ChemicalToDiseaseOrPhenotypicFeatureAssociation",
          "subject": "CHEMBL:CHEMBL1201585",
          "object": "MONDO:0007254"
        },
        "kge3": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "MUC16",
          "object": "MONDO:0007254",
          "value": -0.12169811320754698
        },
        "kge4": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "ABCA8",
          "object": "MONDO:0007254",
          "value": -0.09999999999999983
        },
        "kge5": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "NAV1",
          "object": "MONDO:0007254",
          "value": -0.09999999999999983
        },
        "kge6": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "MYEF2",
          "object": "MONDO:0007254",
          "value": -0.09999999999999983
        },
        "kge7": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "ROBO1",
          "object": "MONDO:0007254",
          "value": -0.09999999999999983
        },
        "kge8": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "DNAH11",
          "object": "MONDO:0007254",
          "value": -0.09999999999999983
        },
        "kge9": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "MYH6",
          "object": "MONDO:0007254",
          "value": -0.09999999999999983
        },
        "kge10": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "CXorf36",
          "object": "MONDO:0007254",
          "value": -0.09999999999999983
        },
        "kge11": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "ARFGEF2",
          "object": "MONDO:0007254",
          "value": -0.09999999999999983
        },
        "kge12": {
          "predicate": "biolink:GeneToDiseaseAssociation",
          "subject": "MYH15",
          "object": "MONDO:0007254",
          "value": -0.09999999999999983
        }
      },
      "nodes": {
        "CHEMBL:CHEMBL1201585": {
          "category": "biolink:Drug",
          "name": "TRASTUZUMAB"
        },
        "MONDO:0007254": {
          "category": "biolink:Disease"
        },
        "EFO:0000714": {
          "category": "biolink:PhenotypicFeature"
        },
        "MUC16": {
          "category": "biolink:Gene",
          "name": "ENSEMBL:ENSG00000181143"
        },
        "ABCA8": {
          "category": "biolink:Gene",
          "name": "ENSEMBL:ENSG00000141338"
        },
        "NAV1": {
          "category": "biolink:Gene",
          "name": "ENSEMBL:ENSG00000134369"
        },
        "MYEF2": {
          "category": "biolink:Gene",
          "name": "ENSEMBL:ENSG00000104177"
        },
        "ROBO1": {
          "category": "biolink:Gene",
          "name": "ENSEMBL:ENSG00000169855"
        },
        "DNAH11": {
          "category": "biolink:Gene",
          "name": "ENSEMBL:ENSG00000105877"
        },
        "MYH6": {
          "category": "biolink:Gene",
          "name": "ENSEMBL:ENSG00000197616"
        },
        "CXorf36": {
          "category": "biolink:Gene",
          "name": "ENSEMBL:ENSG00000147113"
        },
        "ARFGEF2": {
          "category": "biolink:Gene",
          "name": "ENSEMBL:ENSG00000124198"
        },
        "MYH15": {
          "category": "biolink:Gene",
          "name": "ENSEMBL:ENSG00000144821"
        }
      }
    },
    "results": [
      {
        "edge_bindings": {
          "e0": [
            {
              "id": "kge0"
            }
          ],
          "e2": [
            {
              "id": "kge1"
            }
          ]
        },
        "node_bindings": {
          "n0": [
            {
              "id": "CHEMBL:CHEMBL1201585"
            }
          ],
          "n2": [
            {
              "id": "MONDO:0007254"
            }
          ],
          "n3": [
            {
              "id": "EFO:0000714"
            }
          ]
        }
      },
      {
        "edge_bindings": {
          "e0": [
            {
              "id": "kge0"
            }
          ],
          "e1": [
            {
              "id": "kge3"
            }
          ],
          "e2": [
            {
              "id": "kge1"
            }
          ]
        },
        "node_bindings": {
          "n0": [
            {
              "id": "CHEMBL:CHEMBL1201585"
            }
          ],
          "n1": [
            {
              "id": "MUC16"
            }
          ],
          "n2": [
            {
              "id": "MONDO:0007254"
            }
          ],
          "n3": [
            {
              "id": "EFO:0000714"
            }
          ]
        }
      },
      {
        "edge_bindings": {
          "e0": [
            {
              "id": "kge0"
            }
          ],
          "e1": [
            {
              "id": "kge4"
            }
          ],
          "e2": [
            {
              "id": "kge1"
            }
          ]
        },
        "node_bindings": {
          "n0": [
            {
              "id": "CHEMBL:CHEMBL1201585"
            }
          ],
          "n1": [
            {
              "id": "ABCA8"
            }
          ],
          "n2": [
            {
              "id": "MONDO:0007254"
            }
          ],
          "n3": [
            {
              "id": "EFO:0000714"
            }
          ]
        }
      },
      {
        "edge_bindings": {
          "e0": [
            {
              "id": "kge0"
            }
          ],
          "e1": [
            {
              "id": "kge5"
            }
          ],
          "e2": [
            {
              "id": "kge1"
            }
          ]
        },
        "node_bindings": {
          "n0": [
            {
              "id": "CHEMBL:CHEMBL1201585"
            }
          ],
          "n1": [
            {
              "id": "NAV1"
            }
          ],
          "n2": [
            {
              "id": "MONDO:0007254"
            }
          ],
          "n3": [
            {
              "id": "EFO:0000714"
            }
          ]
        }
      },
      {
        "edge_bindings": {
          "e0": [
            {
              "id": "kge0"
            }
          ],
          "e1": [
            {
              "id": "kge6"
            }
          ],
          "e2": [
            {
              "id": "kge1"
            }
          ]
        },
        "node_bindings": {
          "n0": [
            {
              "id": "CHEMBL:CHEMBL1201585"
            }
          ],
          "n1": [
            {
              "id": "MYEF2"
            }
          ],
          "n2": [
            {
              "id": "MONDO:0007254"
            }
          ],
          "n3": [
            {
              "id": "EFO:0000714"
            }
          ]
        }
      },
      {
        "edge_bindings": {
          "e0": [
            {
              "id": "kge0"
            }
          ],
          "e1": [
            {
              "id": "kge7"
            }
          ],
          "e2": [
            {
              "id": "kge1"
            }
          ]
        },
        "node_bindings": {
          "n0": [
            {
              "id": "CHEMBL:CHEMBL1201585"
            }
          ],
          "n1": [
            {
              "id": "ROBO1"
            }
          ],
          "n2": [
            {
              "id": "MONDO:0007254"
            }
          ],
          "n3": [
            {
              "id": "EFO:0000714"
            }
          ]
        }
      },
      {
        "edge_bindings": {
          "e0": [
            {
              "id": "kge0"
            }
          ],
          "e1": [
            {
              "id": "kge8"
            }
          ],
          "e2": [
            {
              "id": "kge1"
            }
          ]
        },
        "node_bindings": {
          "n0": [
            {
              "id": "CHEMBL:CHEMBL1201585"
            }
          ],
          "n1": [
            {
              "id": "DNAH11"
            }
          ],
          "n2": [
            {
              "id": "MONDO:0007254"
            }
          ],
          "n3": [
            {
              "id": "EFO:0000714"
            }
          ]
        }
      },
      {
        "edge_bindings": {
          "e0": [
            {
              "id": "kge0"
            }
          ],
          "e1": [
            {
              "id": "kge9"
            }
          ],
          "e2": [
            {
              "id": "kge1"
            }
          ]
        },
        "node_bindings": {
          "n0": [
            {
              "id": "CHEMBL:CHEMBL1201585"
            }
          ],
          "n1": [
            {
              "id": "MYH6"
            }
          ],
          "n2": [
            {
              "id": "MONDO:0007254"
            }
          ],
          "n3": [
            {
              "id": "EFO:0000714"
            }
          ]
        }
      },
      {
        "edge_bindings": {
          "e0": [
            {
              "id": "kge0"
            }
          ],
          "e1": [
            {
              "id": "kge10"
            }
          ],
          "e2": [
            {
              "id": "kge1"
            }
          ]
        },
        "node_bindings": {
          "n0": [
            {
              "id": "CHEMBL:CHEMBL1201585"
            }
          ],
          "n1": [
            {
              "id": "CXorf36"
            }
          ],
          "n2": [
            {
              "id": "MONDO:0007254"
            }
          ],
          "n3": [
            {
              "id": "EFO:0000714"
            }
          ]
        }
      },
      {
        "edge_bindings": {
          "e0": [
            {
              "id": "kge0"
            }
          ],
          "e1": [
            {
              "id": "kge11"
            }
          ],
          "e2": [
            {
              "id": "kge1"
            }
          ]
        },
        "node_bindings": {
          "n0": [
            {
              "id": "CHEMBL:CHEMBL1201585"
            }
          ],
          "n1": [
            {
              "id": "ARFGEF2"
            }
          ],
          "n2": [
            {
              "id": "MONDO:0007254"
            }
          ],
          "n3": [
            {
              "id": "EFO:0000714"
            }
          ]
        }
      },
      {
        "edge_bindings": {
          "e0": [
            {
              "id": "kge0"
            }
          ],
          "e1": [
            {
              "id": "kge12"
            }
          ],
          "e2": [
            {
              "id": "kge1"
            }
          ]
        },
        "node_bindings": {
          "n0": [
            {
              "id": "CHEMBL:CHEMBL1201585"
            }
          ],
          "n1": [
            {
              "id": "MYH15"
            }
          ],
          "n2": [
            {
              "id": "MONDO:0007254"
            }
          ],
          "n3": [
            {
              "id": "EFO:0000714"
            }
          ]
        }
      }
    ]
  }
}

```
#### Extracting the Statiscally Important Genes
CHP uses a method called Contributions Analysis to analyze gene importance and thereby rank genes. When the probability of the subgraph query (i.e. everything except the gene wildcards) is calculated, it carries with it a probabilistic mass. Contribution analysis tracks the amount of mass each component in our model contributed to the total mass (i.e. that final probability value of the query subgraph). As gene mutations play a significant role in our model, we are able to track each gene mutation's contribution to the total probabillistic mass, allowing us to yield our ranked gene results. The interpretation of these ranked genes should be that they are the genes that contributed most to supporting the given query.

You can extract this information manually from the TRAPI CHP response results section. The first result will always be the standard probability query of the subgraph (not including any genes). We can extract this information with the same *get_outcome_prob* command.

```python
In [15]: client.get_outcome_prob(response)
Out[15]: 0.8412698412698413
```

The next *n* results are the ranked gene graphs where the gene wildcard has been replaced by a gene instantiation by CHP, while also adding an edge weight (contributation value) to the associated *gene_to_disease_association* edge. We can further extract this ranked list of genes with the *get_ranked_wildcards* chp client helper function.

```python
In [16]: ranked = client.get_ranked_wildcards(response)

In [17]: print(json.dumps(ranked, indent=2))
{
  "Biolink:Gene": [
    {
      "weight": -0.12169811320754698,
      "id": "ENSEMBL:ENSG00000181143",
      "name": "MUC16"
    },
    {
      "weight": -0.09999999999999983,
      "id": "ENSEMBL:ENSG00000141338",
      "name": "ABCA8"
    },
    {
      "weight": -0.09999999999999983,
      "id": "ENSEMBL:ENSG00000134369",
      "name": "NAV1"
    },
    {
      "weight": -0.09999999999999983,
      "id": "ENSEMBL:ENSG00000104177",
      "name": "MYEF2"
    },
    {
      "weight": -0.09999999999999983,
      "id": "ENSEMBL:ENSG00000169855",
      "name": "ROBO1"
    },
    {
      "weight": -0.09999999999999983,
      "id": "ENSEMBL:ENSG00000105877",
      "name": "DNAH11"
    },
    {
      "weight": -0.09999999999999983,
      "id": "ENSEMBL:ENSG00000197616",
      "name": "MYH6"
    },
    {
      "weight": -0.09999999999999983,
      "id": "ENSEMBL:ENSG00000147113",
      "name": "CXorf36"
    },
    {
      "weight": -0.09999999999999983,
      "id": "ENSEMBL:ENSG00000124198",
      "name": "ARFGEF2"
    },
    {
      "weight": -0.09999999999999983,
      "id": "ENSEMBL:ENSG00000144821",
      "name": "MYH15"
    }
  ]
}

```

## Drug Wildcard Query (One query, many results)
We hope to support the same type of wildcard queries for drugs/therauptics, but that is not currently supported.

# CHP Query Semantics
TODO: Explain biolink edge semantics and node types

# API Documentation
* [CHP Client API Reference](docs/chp_client_reference.md#docs/chp_client_reference.md#chp-client-reference)
* [CHP API Github Docs](https://github.com/di2ag/ConnectionsHypothesisProviderAPI)
