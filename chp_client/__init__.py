"""
Generic Client for Connections Hypothesis API.
"""

import types
import copy

from chp_client.client import ChpClient
from chp_client._version import __version__

# Function aliases common to all clients
COMMON_ALIASES = {
        "_query": 'query',
        "_predicates": 'predicates',
        "_curies": 'curies',
        "_get_outcome_prob": 'get_outcome_prob',
        "_get_ranked_wildcards": 'get_ranked_wildcards'
        }

# Set reasoner specific aliases

# Object creation kwargs common to all clients
COMMON_KWARGS = {
        "_default_url": 'http://chp.thayer.dartmouth.edu',
        "_query_endpoint": '/query/',
        "_predicates_endpoint": '/predicates/',
        "_curies_endpoint": '/curies/',
        }

# Reasoner specific kwargs
DEFAULT_KWARGS = copy.copy(COMMON_KWARGS)
DEFAULT_KWARGS.update({
        "_reasoner_id": 'default',
        })

CLIENT_SETTINGS = {
        "default": {
                "class_name": 'DefaultClient',
                "class_kwargs": DEFAULT_KWARGS,
                "attr_aliases": COMMON_ALIASES,
                "base_class": ChpClient,
                "mixins": []
                },
        }


def copy_func(f, name=None):
    """
    Return a function with same code, globals, closure, and name (or provided name).
    """
    fn = types.FunctionType(f.__code__, f.__globals__, name or f.__name__,
            f.__defaults__, f.__closure__)
    # If f has been given attributes
    fn.__dict__.update(f.__dict__)
    return fn


def get_client(reasoner_id=None, instance=True, *args, **kwargs):
    """ Function to return a new python client for the CHP API.

    Args:
        reasoner_id: Optional reasoner id for spcific ARA use cases. Will run the chp/integrator/{ara handler}.py.
            If left as None, default handler will be run.
        instance: if True, return an instance of the derived client, if False return the class of the derived
            client.

    All other args/kwargs are passed to the derived client instantiation (if applicable).
    """
    if reasoner_id is None:
        reasoner_id = 'default'
    reasoner_id = reasoner_id.lower()
    if reasoner_id not in CLIENT_SETTINGS:
        raise Exception('No reasoner named {0}, currently available clients are {1}'.format(
                reasoner_id, CLIENT_SETTINGS.keys()))
    _settings = CLIENT_SETTINGS[reasoner_id]
    _class = type(_settings["class_name"], tuple([_settings["base_class"]] + _settings["mixins"]), _settings["class_kwargs"])
    for (src_attr, target_attr) in _settings["attr_aliases"].items():
        if getattr(_class, src_attr, False):
            setattr(_class, target_attr, copy_func(getattr(_class, src_attr), name=target_attr))
    #TODO(Chase): Add docstring support
    _client = _class(*args, **kwargs) if instance else _class
    return _client


class DefaultClient(get_client('default', instance=False)):
    pass
