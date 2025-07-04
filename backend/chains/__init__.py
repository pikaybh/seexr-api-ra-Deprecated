######## PI-Rating ########
from .pi_ratings import ProbabilityImpactRatingV1
from .pi_ratings_test_monarch_w_rag import ProbabilityImpactRatingTestMonarchRAG
from .pi_ratings_test_monarch_wo_rag import ProbabilityImpactRatingTestMonarchWoRAG
from .pi_ratings_test_democrat_w_rag import ProbabilityImpactRatingTestDemocratRAG
from .pi_ratings_test_democrat_wo_rag import ProbabilityImpactRatingTestDemocratWoRAG
from .eval_multi_w_rag import EvalMultiRAG

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
        EvalMultiRAG(ds_num=10),
        EvalMultiRAG(ds_num=55),
        EvalMultiRAG(ds_num=59),
        EvalMultiRAG(ds_num=73),
        EvalMultiRAG(ds_num=98),
        CheckListV1()
    ]
    for _chain in _chains:
        chain = _chain.configure(**kwargs)
        chains.append(chain)
    return chains