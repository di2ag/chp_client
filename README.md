## Introduction
The *chp_client* is a lightweight Python client for the NCATS Connections Hypothesis Provider (CHP). It is meant to be an easy-to-use wrapper utility to both run and build TRAPI queries the CHP web service will understand. Many of the CHP queries have been inspired by direct input from Translator ARAs and such ARAs may have their own dedicated CHP API client that returns results that they expect. However, there is also a default client that can handle generic CHP requests. 

## Requirements
  - Python >= 3.6
  - [requests](https://pypi.python.org/pypi/requests)
  
### Optional libraries
  - [requests_cache](https://pypi.python.org/pypi/requests-cache) *Allows user to setup of requests caching.*

## Installation
### Option 1
``` python3 setup.py install ```
### Option 2
```pip3 install -e git+https://github.com/di2ag/chp_client```

## Quick Start
Once you have installed the CHP client, useage is as simple as:
``` python3
In[1]: from chp_client import get_client

In[2]: default_client = get_client()
```

Now that you have an instance of the client, you can determine which query graph edge predicates are currently supported by CHP with:

```python3
In[3]: default_client.predicates()

```

And you can check the supported curies by:

```python3
In[4]: default_client.curies()
```
This function will return a dictionary of supported biolink entities (NamedThings) that are supported by CHP along with a list of curies for each type. The list will include both our internal CHP name for the entity along with its associated curie for better human readability. *Note: When building query graphs only specify the appropriate curie. There is no need to also specify our internal name that we provide.*

Now that we know which curies and predicates are supported by CHP we can post a query to CHP via:

```python3
In[5]: default_client.query(q)
```
In the next section we will look at how to build CHP queries.

## Building Supported CHP Queries
As CHP is TRAPI complinent a large subset of queries can be built with a wide variety of structures. In order to scope the query building problem, we have currently limited the structures of queries that can be asked and have detailed their respective semantics. *Note: A Translator and the Biolink model develop we intend to ease these restrictions.*

### Standard Probablistic Query (One query graph, one result)
TODO: single node of each type queries.
TODO: multiple node of each type queries.

### Gene Wildcard Query (One query, many results)
TODO: Contribution analysis ranked genes

### Drug Wildcard Query (One query, many results)
To come...


## CHP Query Semantics
TODO: Explain biolink edge semantics and node types

## API Documentation
TODO.
