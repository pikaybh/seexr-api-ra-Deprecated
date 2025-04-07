import requests

from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel

from structures import KrasRiskAssessmentOutput, KrasRiskAssessmentOutputV2, kras_map
from models import ChainBase


async def law_classification(hazard: str, mitigations: list):
    """
    Classify the law based on the hazard and mitigation measures.
    """
    mitigations_str = "\n".join([f"{i}. {v}" for i, v in enumerate(mitigations, 1)])
    url = f"http://localhost:8001/predictLaw/?hazard_str={hazard}&mitigation_str={mitigations_str}"
    print(f"{url = }")
    response = requests.get(url)
    print(f"{response.text = }")
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print(f"Error: {response.status_code}")
        return None
    

async def get_law_classification(feed: KrasRiskAssessmentOutputV2):
    """
    Get the law classification for each risk item in the feed.
    """
    fedd_dict = BaseModel.model_dump(feed)
    for k, v in fedd_dict.items():
        if k.strip().startswith("위험성평가표"):
            for i in range(len(v)):
                item = v[i]
                hazard = item["유해위험요인"]
                mitigation = item["감소대책"]
                if hazard and mitigation:
                    law_classification_result = await law_classification(hazard, mitigation)
                    if law_classification_result:
                        item["관련근거"] = law_classification_result
                        print(f"Law classification result for item {i} in {k}: {law_classification_result}")
                else:
                    print(f"Error: Hazard or mitigation is empty for item {i} in {k}")
                    item["관련근거"] = "-"
    
    return fedd_dict



class RMA(ChainBase):
    async def chain_call(self, model, embeddings):
        self.model = model
        self.embeddings = embeddings

        # Output Configuration
        structured_output = self.model.with_structured_output(KrasRiskAssessmentOutputV2)

        # Retrieval
        reference_retriever = self.faiss_retrieval(file_name="faiss_KRAS")

        # Prompt
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

        # Input Configuration
        chain_init = self.parallel_init({
            "image_paths": lambda x: self.image_preprocessor(x.get("image_paths", [])),
            "count": lambda x: x["count"],
            "work_type": lambda x: x["work_type"],
            "procedure": lambda x: x["procedure"],
            "reference": self.get_dict2str(mapping=kras_map) | RunnablePassthrough() | reference_retriever | self.format_docs,
        })

        # Chain Configuration
        chain = chain_init | prompt_template | structured_output | self.printer | get_law_classification | self.printer

        return chain



__all__ = ["RMA"]

if __name__ == "__main__":
    import asyncio
    from utils import pretty_print_risk_evaluation

    chain =  asyncio.run(
        RMA().chain_call(
            model="openai/gpt-4o", 
            embeddings="openai/text-embedding-ada-002"
        )
    )
    result = asyncio.run(
        chain.ainvoke(
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
    )
    for k, v in dict(result).items():
        if k.strip().startswith("위험성평가표"):
            print(f"- {k}:")
            for i in v:
                print(f"  - {i}")
        else:
            print(f"- {k}: {v}")
    pretty_print_risk_evaluation(result.공종, result.공정, result.작업명, result.위험성평가표, result.기타)
