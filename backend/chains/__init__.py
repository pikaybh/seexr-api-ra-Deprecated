######## PI-Rating ########
from .pi_ratings import ProbabilityImpactRatingV1
from .pi_ratings_test import ProbabilityImpactRatingTest
from .pi_ratings_test_wo_rag import ProbabilityImpactRatingTestWoRAG

######## Checklist ########
from .checklists import CheckListV1


__all__ = ["configure_chains"]


def configure_chains(chains: list = [], **kwargs) -> list:
    _chains = [
        ProbabilityImpactRatingV1(),
        ProbabilityImpactRatingTest(),
        ProbabilityImpactRatingTestWoRAG(),
        CheckListV1()
    ]
    for _chain in _chains:
        chain = _chain.configure(**kwargs)
        chains.append(chain)
    return chains