from langchain_core.runnables import RunnablePassthrough

from structures import KrasRiskAssessmentOutput, kras_map
from models import ChainBase



class RMA(ChainBase):
    def chain_call(self, model, embeddings):
        self.model = model
        self.embeddings = embeddings

        # Output Configuration
        structured_output = self.model.with_structured_output(KrasRiskAssessmentOutput)

        # Retrieval
        reference_retriever = self.faiss_retrieval(file_name="faiss_KRAS")
        # regulation_retriever = self.faiss_retrieval(file_name="faiss_law_openai")

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
                # related_law="{related_law}"
            ))
        ])

        # Input Configuration
        chain_init = self.parallel_init({
            "image_paths": lambda x: self.image_preprocessor(x.get("image_paths", [])),
            "count": lambda x: x["count"],
            "work_type": lambda x: x["work_type"],
            "procedure": lambda x: x["procedure"],
            "reference": self.get_dict2str(mapping=kras_map) | RunnablePassthrough() | reference_retriever | self.format_docs,
            # "related_law": self.get_dict2str(mapping=kras_map) | RunnablePassthrough() | regulation_retriever | self.format_docs,
        })

        # Chain Configuration
        chain = chain_init | prompt_template | structured_output | self.printer

        return chain



__all__ = ["RMA"]

if __name__ == "__main__":
    from utils import pretty_print_risk_evaluation

    result = RMA().chain_call(
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
    pretty_print_risk_evaluation(result.공종, result.공정, result.작업명, result.위험성평가표, result.기타)
