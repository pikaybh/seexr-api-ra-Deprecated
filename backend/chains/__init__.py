######## PI-Rating ########
from .pi_ratings import ProbabilityImpactRatingV1
from .pi_ratings_test_monarch_w_rag import ProbabilityImpactRatingTestMonarchRAG
from .pi_ratings_test_monarch_wo_rag import ProbabilityImpactRatingTestMonarchWoRAG
from .pi_ratings_test_democrat_w_rag import ProbabilityImpactRatingTestDemocratRAG
from .pi_ratings_test_democrat_wo_rag import ProbabilityImpactRatingTestDemocratWoRAG

######## Checklist ########
from .checklists import CheckListV1


__all__ = ["configure_chains"]


def configure_chains(chains: list = [], **kwargs) -> list:
    _chains = [
        ProbabilityImpactRatingV1(),
        ProbabilityImpactRatingTestMonarchRAG(),
        ProbabilityImpactRatingTestMonarchWoRAG(),
        ProbabilityImpactRatingTestDemocratRAG(),
        ProbabilityImpactRatingTestDemocratWoRAG(),
        CheckListV1()
    ]
    for _chain in _chains:
        chain = _chain.configure(**kwargs)
        chains.append(chain)
    return chains