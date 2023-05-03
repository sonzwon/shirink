import itertools
from typing import Dict, List


def dict_filter(d: Dict, filter_list: List):
    filtered = {}
    for k, v in d.items():
        if k in filter_list:
            filtered[k] = v
    return filtered


def dict_slice(d: Dict, n: int):
    return dict(itertools.islice(d.items(), n))
