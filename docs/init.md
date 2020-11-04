# CHP Client Module
This is a helper module to allow CHP users to quickly build, load, and save CHP supported JSON queries.

## Methods

### chp_client.get_client
```python
get_client(reasoner_id=None, instance=True)       
```
> Function to return a new python client for the CHP API.
>
> **Parameters:**
> * **reasoner_id:** *str*
>   * A reasoner (ARA) string identifier. Only use if you have been explicitly instructed by CHP support.
> * **instance:** *bool*
>   * if True, return an instance of the derived client, if False return the class of the derived
            client.
>
> **Returns:** 
> * **out:** `ChpClient`
>   * Returns an instantiation of a [ChpClient](client.md#chp_clientclientchpclient)

#### Notes:

#### Examples:
```python
In [1]: from chp_client import get_client

In [2]: default_client = get_client()
```
