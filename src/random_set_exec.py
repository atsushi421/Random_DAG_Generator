import networkx as nx
import numpy as np
import random
import copy

from typing import List

from src.chain import Chain
from src.utils import choice_one_from_cfg
from src.abbreviation import ToO, ToA


def random_set_exec(cfg, G: nx.DiGraph, chains: List[Chain]=[]) -> None:
    def random_get_exec(node_i: int) -> int:
        if('Fixed' in cfg['Execution time'].keys()):
            return cfg['Execution time']['Fixed']

        ### Determine upper bound
        upper_bound = None
        if(ToO['UMP'] in cfg.keys()
                and ToO['MREP'] in cfg[ToO['UMP']].keys()
                and 'period' in list(G.nodes[node_i].keys())):
            upper_bound = int(np.ceil(G.nodes[node_i]['period']
                                      * choice_one_from_cfg(cfg[ToO['UMP']][ToO['MREP']])))

        ### choices - upper bound
        choices = cfg['Execution time']['Random']
        if(upper_bound):
            choices = [p for p in choices if p <= upper_bound]

        return random.choice(choices)

    if(ToO['UMP'] in cfg.keys()
            and cfg[ToO['UMP']][ToO['PT']] == 'Chain'):
        pass # TODO
    else:
        for node_i in G.nodes():
            G.nodes[node_i]['exec'] = random_get_exec(node_i)