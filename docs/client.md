# CHP Client Client Module
This module handles all the CHP endpoint wrapper functions.

## Classes
### chp_client.client.ChpClient
```python
class ChpClient(url=None)        
```
> The client for the CHP API web service.
> 
> **Parameters:**
> * **url:** *str*
>   * A string url that will overwrite the default CHP urls. Don't use unless you are sure you need to.

#### Methods

##### ChpClient.query
```python
ChpClient.query(q, max_results=10)        
```
> This is the wrapper for the POST query of CHP web service and returns the query result.
>
> **Parameters:**
> * **q:** *dict*
>   * a JSON TRAPI query.
> * **max_results:** *int* 
>   * the maximum number of results to return. Only applicable for wildcard queries. Default: 10.
>
> **Returns:**
> * **out:** *dict*
>   * A dict JSON response query.

###### Examples:
``` python3
In [1]: from chp_client import get_client

In [2]: default_client = get_client()

In[3]: default_client.query(q)
{
  "message": {
    "query_graph": {
      "edges": {
        "e0": {
          "type": "gene_to_disease_association",
          "source_id": "n0",
          "target_id": "n2"
        },
        "e1": {
          "type": "chemical_to_disease_or_phenotypic_feature_association",
          "source_id": "n1",
          "target_id": "n2"
        },
        "e2": {
          "type": "disease_to_phenotypic_feature_association",
          "source_id": "n2",
          "target_id": "n3",
          "properties": {
            "qualifier": ">=",
            "value": 500
          }
        }
      },
      "nodes": {
        "n0": {
          "type": "gene",
          "curie": "ENSEMBL:ENSG00000132155"
        },
        "n1": {
          "type": "chemical_substance",
          "curie": "CHEMBL:CHEMBL1201585"
        },
        "n2": {
          "type": "disease",
          "curie": "MONDO:0007254"
        },
        "n3": {
          "type": "phenotypic_feature",
          "curie": "EFO:0000714"
        }
      }
    },
    "knowledge_graph": {
      "edges": {
        "kge0": {
          "type": "gene_to_disease_association",
          "source_id": "ENSEMBL:ENSG00000132155",
          "target_id": "MONDO:0007254"
        },
        "kge1": {
          "type": "chemical_to_disease_or_phenotypic_feature_association",
          "source_id": "CHEMBL:CHEMBL1201585",
          "target_id": "MONDO:0007254"
        },
        "kge2": {
          "type": "disease_to_phenotypic_feature_association",
          "source_id": "MONDO:0007254",
          "target_id": "EFO:0000714",
          "properties": {
            "qualifier": ">=",
            "value": 500
          },
          "has_confidence_level": 1.0
        }
      },
      "nodes": {
        "ENSEMBL:ENSG00000132155": {
          "type": "gene",
          "name": "RAF1"
        },
        "CHEMBL:CHEMBL1201585": {
          "type": "chemical_substance",
          "name": "TRASTUZUMAB"
        },
        "MONDO:0007254": {
          "type": "disease"
        },
        "EFO:0000714": {
          "type": "phenotypic_feature"
        }
      }
    },
    "results": [
      {
        "node_bindings": {
          "n0": {
            "kg_id": "ENSEMBL:ENSG00000132155"
          },
          "n1": {
            "kg_id": "CHEMBL:CHEMBL1201585"
          },
          "n2": {
            "kg_id": "MONDO:0007254"
          },
          "n3": {
            "kg_id": "EFO:0000714"
          }
        },
        "edge_bindings": {
          "e0": {
            "kg_id": "kge0"
          },
          "e1": {
            "kg_id": "kge1"
          },
          "e2": {
            "kg_id": "kge2"
          }
        }
      }
    ]
  }
}
```

##### ChpClient.predicates
```python
ChpClient.predicates()        
```
> Returns a dictionary of available query edge predicates that are currently supported.
>
> **Returns:**
> * **out:** *dict*
>   * A dictionary of available CHP supported predicates.

``` python3
In [1]: from chp_client import get_client

In [2]: default_client = get_client()

In[3]: default_client.predicates()
{
  "gene": {
    "disease": [
      "gene_to_disease_association"
    ]
  },
  "chemical_substance": {
    "disease": [
      "chemical_to_disease_or_phenotypic_feature_association"
    ]
  },
  "disease": {
    "phenotypic_feature": [
      "disease_to_phenotypic_feature_association"
    ]
  }
}
```

##### ChpClient.curies
```python
ChpClient.curies()        
```
> Returns a dictionary of available node curies that are currently supported.
>
> **Returns:**
> * **out:** *dict*
>   * A dictionary of available CHP supported curies.

###### Examples
``` python3
In [1]: from chp_client import get_client

In [2]: default_client = get_client()

In [3]: default_client.curies()
{
  "chemical_substance": [
    {
      "name": "ZOLADEX",
      "curie": "CHEMBL:CHEMBL1201247"
    },
    {
      "name": "CYCLOPHOSPHAMIDE",
      "curie": "CHEMBL:CHEMBL88"
    }, ...
  ]
  "phenotypic_feature": [
    {
      "name": "survival_time",
      "curie": "EFO:0000714"
    }
  ],
  "disease": [
    {
      "name": "breast_cancer",
      "curie": "MONDO:0007254"
    }
  ],
  "gene": [
    {
      "name": "CLIP2",
      "curie": "ENSEMBL:ENSG00000106665"
    },
    {
      "name": "PI4KA",
      "curie": "ENSEMBL:ENSG00000241973"
    },
    {
      "name": "CELSR2",
      "curie": "ENSEMBL:ENSG00000143126"
    }, ...
  ]
}
```
