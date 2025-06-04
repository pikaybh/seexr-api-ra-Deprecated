######## PI-Rating ########
from .pi_ratings import ProbabilityImpactRatingV1
from .pi_ratings_test import ProbabilityImpactRatingTest

######## Checklist ########
from .checklists import CheckListV1


__all__ = ["configure_chains"]


def configure_chains(chains: list = [], **kwargs) -> list:
    _chains = [
        ProbabilityImpactRatingV1(),
        ProbabilityImpactRatingTest(),
        CheckListV1()
    ]
    for _chain in _chains:
        chain = _chain.configure(**kwargs)
        chains.append(chain)
    return chains