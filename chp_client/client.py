"""
Python Client for generic CHP API services.
"""

from collections import defaultdict
from chp_client._version import __version__
from chp_client.trapi_constants import *

import requests
import sys
import warnings

try:
    import requests_cache
    caching_avail = True
except ImportError:
    caching_avail = False

class ChpClient:
    """
    The client for the CHP API web service.
    """

    def __init__(self, url=None):

        if url is None:
            url = self._default_url
        self.url = url
        self._cached = False

        # check for appropriate version
        package_versions = self._versions(verbose=True)
        endpoint_version = package_versions['chp_client']
        endpoint_version_split = [int(x) for x in endpoint_version.split('.')]
        local_version_split = [int(x) for x in __version__.split('.')]
        if endpoint_version_split[0] != local_version_split[0]:
            sys.exit('Major version deviation in chp_client. Please update chp_client to grab the newest version')
        elif endpoint_version_split[1] != local_version_split[1]:
            sys.exit('Minor version deviation in chp_client. Please update chp_client to grab the newest version')
        elif endpoint_version_split[2] != local_version_split[2]:
            warnings.warn('Patch version deviation in chp_client. Please update chp_client to grab the newest version or run at your own risk!')

    def _get(self, url, params=None, verbose=True):
        params = params or {}
        res = requests.get(url, json=params)
        from_cache = getattr(res, 'from_cache', False)
        ret = res.json()
        return from_cache, ret

    def _post(self, url, params, verbose=True):
        res = requests.post(url, json=params)
        from_cache = getattr(res, 'from_cache', False)
        ret = res.json()
        return from_cache, ret

    def _query_all(self, queries, **kwargs):
        """ Return the query result.
        This is the wrapper for the POST query_all of CHP web service.

        Args:
            queries: a list of JSON TRAPI queries.
            max_results: the maximum number of results to return. Only applicable for wildcard queries.
                Default: 10.
        """
        _url = self.url + self._query_all_endpoint
        # First pop off the message and combine them
        q = {"message": []}
        for query in queries:
            q["message"].append(query.pop("message"))
        verbose = kwargs.pop('verbose', True)
        q["max_results"] = kwargs.pop('max_results', 10)
        q["client_id"] = self._client_id
        from_cache, out = self._post(_url, q, verbose=verbose)
        if verbose and from_cache:
            print('Result from cache.')
        return out

    def _query(self, q, **kwargs):
        """ Return the query result.
        This is the wrapper for the POST query of CHP web service.

        Args:
            q: a JSON TRAPI query.
            max_results: the maximum number of results to return. Only applicable for wildcard queries.
                Default: 10.
        """
        _url = self.url + self._query_endpoint
        verbose = kwargs.pop('verbose', True)
        q["max_results"] = kwargs.pop('max_results', 10)
        q["client_id"] = self._client_id
        from_cache, out = self._post(_url, q, verbose=verbose)
        if verbose and from_cache:
            print('Result from cache.')
        return out

    def _predicates(self, verbose=True, **kwargs):
        """ Returns a dictionary of available query edge predicates that are currently supported.
        """
        _url = self.url + self._predicates_endpoint
        from_cache, ret = self._get(_url, verbose=verbose)
        if verbose and from_cache:
            print('Result from cache.')
        return ret

    def _constants(self, verbose=True, **kwargs):
        """ Returns a dictionary of TRAPI constants to be used in query building.
        """
        _url = self.url + self._constants_endpoint
        from_cache, ret = self._get(_url, verbose=verbose)
        if verbose and from_cache:
            print('Result from cache.')
        return ret

    def _curies(self, verbose=True, **kwargs):
        """ Returns a dictionary of available node curies that are currently supported.

        Structure is:
            { biolinkEntity: [
                        {
                            name: Name we use internally in CHP (Good for human readable results).
                            curie: Curie of the given entity.
                        }, ...
                    ]
            }

        Example:
            {"gene": [
                {"name": 'RAF1',
                 "curie": 'ENSEMBL:ENSG00000132155'},
                {"name": 'MAP3K13',
                 "curie": ''ENSEMBL:ENSG00000073803'},
                 ...
                 ],
            "chemical_substance": [
                {"name": 'cyclophosphamide',
                 "curie": ''CHEMBL:CHEMBL88'},
                 ...
                 ],
            ...
            }
        """
        _url = self.url + self._curies_endpoint
        # Send reasoner_id in get payload
        payload = {"client_id": self._client_id}
        from_cache, ret = self._get(_url, params=payload, verbose=verbose)
        if verbose and from_cache:
            print('Result from cache.')
        return ret

    def _versions(self, verbose=True, **kwargs):
        """ Returns a dictionary of all enpoint dependency versions
        """
        _url = self.url + self._versions_endpoint
        from_cache, ret = self._get(_url, verbose=verbose)
        if verbose and from_cache:
            print('Result from cache.')
        return ret

    def _get_outcome_prob(self, q_resp):
        """ Extracts the probability from a CHP query response.
        """
        # Extract response. Probability is always in first result
        message = q_resp["message"]
        kg = message["knowledge_graph"]
        res = message["results"][0]
        # Find the outcome edge
        for qg_id, edge_bind  in res["edge_bindings"].items():
            edge = kg["edges"][edge_bind[0]["id"]]
            if edge["predicate"] == BIOLINK_DISEASE_TO_PHENOTYPIC_FEATURE_PREDICATE:
                try:
                    prob = edge["attributes"][0]["value"]
                    break
                except KeyError:
                    raise KeyError('Could not find associated probability of query. Possible ill-formed query.')
        return prob

    def _get_ranked_wildcards(self, q_resp):
        """ Extracts ranked list of wildcards from a CHP query response.
        """
        if len(q_resp["message"]["results"]) < 2:
            raise ValueError('Could not find any wildcard results. Possible ill-formed query. Consult documentation.')
        qg = q_resp["message"]["query_graph"]
        kg = q_resp["message"]["knowledge_graph"]
        res = q_resp["message"]["results"][1:]
        # Extract wildcard types from qg. Numbers are how many wildcard of each type are in qg.
        wildcard_types = defaultdict(int)
        for node_id, node in qg["nodes"].items():
            if "id" not in node:
                wildcard_types[node["category"]] += 1
        ranks = defaultdict(list)
        for _res in res:
            for qg_id, edge_bind in _res["edge_bindings"].items():
                edge = kg["edges"][edge_bind[0]["id"]]
                if "biolink:Gene" in wildcard_types and edge["predicate"] == BIOLINK_GENE_TO_DISEASE_PREDICATE:
                    weight = edge["attributes"][0]["value"]
                    node_curie = edge["subject"]
                    source_node = kg["nodes"][node_curie]
                    name = source_node["name"]
                    ranks["gene"].append({
                            "weight": weight,
                            "curie": node_curie,
                            "name": name})
                elif "biolink:Drug" in wildcard_types and edge["predicate"] == BIOLINK_CHEMICAL_TO_DISEASE_OR_PHENOTYPIC_FEATURE_PREDICATE:
                    weight = edge["attributes"]["value"]
                    node_curie = edge["subject"]
                    source_node = kg["nodes"][node_curie]
                    name = source_node["name"]
                    ranks["gene"].append({
                            "weight": weight,
                            "curie": node_curie,
                            "name": name})
                else:
                    continue
        return ranks

    def _set_caching(self, cache_db=None, verbose=True, **kwargs):
        '''Installs a local cache for all requests.
            **cache_db** is the path to the local sqlite cache database.'''
        if caching_avail:
            if cache_db is None:
                cache_db = self._default_cache_file
            requests_cache.install_cache(
                cache_name=cache_db, allowable_methods=(
                    'GET', 'POST'), **kwargs)
            self._cached = True
            if verbose:
                print(
                    '[ Future queries will be cached in "{0}" ]'.format(
                        os.path.abspath(
                            cache_db + '.sqlite')))
        else:
            print("Error: The requests_cache python module is required to use request caching.")
            print("See - https://requests-cache.readthedocs.io/en/latest/user_guide.html#installation")
        return

    def _stop_caching(self):
        '''Stop caching.'''
        if self._cached and caching_avail:
            requests_cache.uninstall_cache()
            self._cached = False
        return

    def _clear_cache(self):
        ''' Clear the globally installed cache. '''
        try:
            requests_cache.clear()
        except AttributeError:
            # requests_cache is not enabled
            print("requests_cache is not enabled. Nothing to clear.")
