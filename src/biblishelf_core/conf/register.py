from collections import OrderedDict

_pools = OrderedDict(
    (
        ('generate', OrderedDict()),
    )
)

class UnknownRegister(KeyError):
    pass


def iter_callback(register_key):
    if register_key not in _pools:
        raise UnknownRegister
    for key, func in _pools[register_key].items():
        return func


def register_callback(register_key, func):
    if register_key not in _pools:
        raise UnknownRegister
    _pools[register_key][id(func)] = func

def unregister_callback(register_key, func):
    if register_key not in _pools:
        raise UnknownRegister
    if id(func) in _pools[register_key]:
        del _pools[register_key][id(func)]