"""
Python Client for generic CHP API services.
"""

from collections import defaultdict

import requests

try:
    import requests_cache
    caching_avail = True
except ImportError:
    caching_avail = False


__version__ = '0.0.1'


class ChpClient:
    """
    The client for the CHP API web service.
    """

    def __init__(self, url=None):
        if url is None:
            url = self._default_url
        self.url = url
        self._cached = False

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
        q["message"]["reasoner_id"] = self._reasoner_id
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
        payload = {"reasoner_id": self._reasoner_id}
        from_cache, ret = self._get(_url, params=payload, verbose=verbose)
        if verbose and from_cache:
            print('Result from cache.')
        return ret

    def _get_outcome_prob(self, q_resp):
        """ Extracts the probability from a CHP query response.
        """
        # Extract response. Probability is always in first result
        kg = q_resp["message"]["knowledge_graph"]
        res = q_resp["message"]["results"][0]
        # Find the outcome edge
        for qg_id, edge_bind  in res["edge_bindings"].items():
            edge = kg["edges"][edge_bind["kg_id"]]
            if edge["type"] == 'disease_to_phenotypic_feature_association':
                try:
                    prob = edge["has_confidence_level"]
                    break
                except KeyError:
                    raise KeyError('Could not find associated probability of query. Possible ill-formed query.')
        return prob

    def _get_ranked_wildcards(self, q_resp):
        """ Extracts ranked list of wildcards from a CHP query response.
        """
        if len(q_resp["results"]) < 2:
            raise ValueError('Could not find any wildcard results. Possible ill-formed query. Consult documentation.')
        qg = q_resp["message"]["query_graph"]
        kg = q_resp["message"]["knowledge_graph"]
        res = q_resp["message"]["results"][1:]
        # Extract wildcard types from qg. Numbers are how many wildcard of each type are in qg.
        wildcard_types = defaultdict(int)
        for node_id, node in qg["nodes"].items():
            if "curie" not in node:
                wildcard_types[node["type"]] += 1
        ranks = defaultdict(list)
        for _res in res:
            for qg_id, edge_bind in _res["edge_bindings"].items():
                edge = kg["edges"][edge_bind["kg_id"]]
                if "gene" in wildcard_types and edge["type"] == 'gene_to_disease_association':
                    weight = edge["weight"]
                    node_curie = edge["source_id"]
                    source_node = kg["nodes"][node_curie]
                    name = source_node["name"]
                    ranks["gene"].append({
                            "weight": weight,
                            "curie": node_curie,
                            "name": name})
                elif "chemical_substance" in wildcard_types and edge["type"] == 'chemical_to_disease_or_phenotypic_feature_association':
                    weight = edge["weight"]
                    node_curie = edge["source_id"]
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
