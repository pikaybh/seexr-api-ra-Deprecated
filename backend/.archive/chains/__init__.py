# from .ra import *
# from .rma import *
# from .rma_v2 import *
# from .rma_v3 import *
# from .rma_text import *

######## TEST ########
# from .dummy_v1_0_1 import *
# from .dummy_v1_1_1 import *
# from .rma_cy_v1 import *
# from .rma_by_v2 import *

######## PI-Rating ########
from .pi_ratings import ProbabilityImpactRatingV1

######## Checklist ########
from .checklists import CheckListV1

__all__ = ["configure_chains"]


def configure_chains(chains: list = [], **kwargs) -> list:
    _chains = [
        ProbabilityImpactRatingV1(),
        CheckListV1()
    ]
    for _chain in _chains:
        chain = _chain.configure(**kwargs)
        chains.append(chain)
    return chains