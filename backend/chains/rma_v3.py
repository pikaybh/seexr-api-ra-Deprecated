import requests
# import socket
from typing import List, Optional

from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel

from structures import KrasRiskAssessmentOutputV2, kras_map
from models import ChainBase
from utils import get_logger


logger = get_logger(__name__)

# LOCAL_IP = requests.get("http://ifconfig.me").text.strip()
# 
# 
# def get_local_ip():
#     """
#     Get the local IP address of the machine.
#     """
#     hostname = socket.gethostname()
#     local_ip = socket.gethostbyname(hostname)
#     return local_ip


def law_classification(
        work_type: str,
        work_process: str,
        hazard: str, 
        mitigations: List[str],
        equipment: Optional[str] = "",
        material: Optional[str] = ""
    ):
    """
    Classify the law based on the hazard and mitigation measures.
    """
    mitigations_str = "\n".join([f"{i}. {v}" for i, v in enumerate(mitigations, 1)])
    url = f"http://snucem1.iptime.org:8001/predictLaw?work_type_str={work_type}&work_process_str={work_process}&eqpt_str={equipment}&mat_str={material}&hazard_str={hazard}&mitigation_str={mitigations_str}"
    # print(f"{url = }")
    response = requests.get(url)
    # print(f"{response.text = }")
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        logger.error(f"Error: {response.status_code}")
        return f"API Error ({response.status_code = })"
    

def get_law_classification(feed: KrasRiskAssessmentOutputV2):
    """
    Get the law classification for each risk item in the feed.
    """
    fedd_dict = BaseModel.model_dump(feed)
    for k, v in fedd_dict.items():
        if k.strip().startswith("위험성평가표"):
            for i in range(len(v)):
                item = v[i]
                work_type = item["공종"]
                work_process = item["공정"]
                equipment = item["설비"]
                material = item["물질"]
                hazard = item["유해위험요인"]
                mitigation = item["감소대책"]
                if hazard and mitigation:
                    law_classification_result = law_classification(
                        work_type=work_type,
                        work_process=work_process,
                        hazard=hazard, 
                        mitigations=mitigation,
                        equipment=equipment,
                        material=material
                    )
                    if law_classification_result:
                        item["관련근거"] = law_classification_result
                        logger.debug(f"Law classification result for item {i} in {k}: {law_classification_result}")
                else:
                    logger.error(f"Error: Hazard or mitigation is empty for item {i} in {k}")
                    item["관련근거"] = "-"
    
    return fedd_dict

from langchain_core.runnables import RunnableParallel, RunnableLambda

class RMAv3(ChainBase):
    def chain_call(self, model, embeddings):
        self.model = model
        self.embeddings = embeddings

        structured_output = self.model.with_structured_output(KrasRiskAssessmentOutputV2)
        reference_retriever = self.faiss_retrieval(file_name="faiss_KRAS")

        self.prompt = "rma2"
        prompt_template = self.template_call("chat", [
            ("system", self.prompt["system"]),
            ("user", "{image_paths}"),
            ("user", self.prompt["user"].format(
                work_type="{work_type}",
                procedure="{procedure}",
                count="{count}",
                reference="{reference}",
            ))
        ])

        # ⚠️ 핵심 체인 정의 (하나의 공정에 대해 동작)
        def single_chain_fn(inputs):
            proc = inputs["procedure"]
            chain_init = {
                "image_paths": lambda x: x.get("image_paths", []),
                "count": lambda x: x.get("count", "1"),
                "work_type": lambda x: x.get("work_type", ""),
                "procedure": lambda _: proc,
                "reference": (
                    self.get_dict2str(mapping=kras_map)
                    | RunnablePassthrough()
                    | reference_retriever
                    | self.format_docs
                )
            }
            full_chain = chain_init | prompt_template | structured_output
            return full_chain.invoke(inputs)

        # ⚠️ procedure 리스트 받아서 parallel 실행
        def orchestrator(all_inputs):
            procedures = all_inputs["procedure"]
            parallel_inputs = []
            for proc in procedures:
                inp = {
                    "image_paths": all_inputs["image_paths"],
                    "count": all_inputs["count"],
                    "work_type": all_inputs["work_type"],
                    "procedure": proc
                }
                parallel_inputs.append(inp)
            # RunnableLambda를 리스트로 감싸서 RunnableParallel 실행
            chains = [RunnableLambda(single_chain_fn) for _ in parallel_inputs]
            parallel_chain = RunnableParallel(*chains)
            return parallel_chain.invoke(parallel_inputs)

        # ⚠️ 전체 체인 정의
        chain = RunnableLambda(orchestrator) | get_law_classification | self.printer

        return chain




__all__ = ["RMAv3"]

if __name__ == "__main__":
    from utils import pretty_print_risk_evaluation

        
    result = RMAv3().chain_call(
        model="openai/gpt-4o", 
        embeddings="openai/text-embedding-ada-002"
    ).invoke(
        {
            "image_paths": [
                "https://i.ytimg.com/vi/qZAB_yWWbU8/maxresdefault.jpg", 
                "https://lh5.googleusercontent.com/proxy/3Bn2dIDlQPZVwEmlBAPO4zafsqgJqm3kmwgBogbS9rMxjJrmHjODRLifzbxHnHkvRK9DLFN0XPnJvT8CiMvRoQ"
            ], 
            "count": "10", 
            "work_type": "철근 작업", 
            "procedure": "자재 운반"
        }
    )
    for k, v in dict(result).items():
        if k.strip().startswith("위험성평가표"):
            logger.info(f"- {k}:")
            for i in v:
                logger.info(f"  - {i}")
        else:
            logger.info(f"- {k}: {v}")
    pretty_print_risk_evaluation(result.공종, result.공정, result.작업명, result.위험성평가표, result.기타)
