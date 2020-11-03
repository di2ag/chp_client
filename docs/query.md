# CHP Client Query Module
This is a helper module to allow CHP users to quickly build, load, and save CHP supported JSON queries.

## Methods

### chp_client.query.build_query
```python
build_query(genes=None, therapeutic=None, outcome=None, disease=None, num_gene_wildcards=0, therapeutic_wildcard=False)        
```
> Helper function to build CHP JSON queries.
>
> **Parameters:**
> * **genes:** *list of strs*
>   * A list of ENSEMBL gene curies (max 10).
> * **therapeutic:** *str* 
>   * A string CHEMBL curie for a drug/therputic.
> * **outcome:** *tuple of form (str, str, str or float)*
>   * A patient outcome tuple of the form ({outcome curie}, {numerical inequality}, {float}).
> * **disease:** *str*
>   * A MONDO disease curie string.
> * **num_gene_wildcards:** *int*
>   * Number of gene wildcards that will be filled by CHP. Default: 0.
> * **therapeutic_wildcard:** *bool*
>   * Boolean letting CHP know if it should try to find a statistically important therapeutic. Default: False.

#### Notes:
* Currently therapeutic wild cards are not supported.

#### Examples:
```python
In [1]: from chp_client.query import build_query

In [2]: q = build_query(
   ...: genes=['ENSEMBL:ENSG00000132155'],
   ...: therapeutic='CHEMBL:CHEMBL1201585',
   ...: disease='MONDO:0007254',
   ...: outcome=('EFO:0000714', '>=', 500)
   )
```
   
### chp_client.query.load_query
```python
load_query(filename)        
```
> Loads a saved JSON query.
>
> **Parameters:**
> * **filename:** *str*
>   * The string file path to the saved JSON query.

#### Notes:

### chp_client.query.save_query
```python
load_query(q, filename)        
```
> Saves JSON query to a specified filename.
>
> **Parameters:**
> * **q:** *dict*
>   * A json query from *build_query* or response from CHP.
> * **filename:** *str*
>   * The string file path to the saved JSON query.

#### Notes:
