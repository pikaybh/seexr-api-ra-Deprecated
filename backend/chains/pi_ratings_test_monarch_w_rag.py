"""250603_위험성평가 체인"""

from langchain_core.runnables import RunnablePassthrough

from schemas import RiskAssessmentEvalInputV2, RiskAssessmentEvalOutputV3, risk_assessment_map
from models import ChainBase
from utils import get_logger


logger = get_logger(__name__)



class ProbabilityImpactRatingTestMonarchRAG(ChainBase):
    def chain_call(self, model, embeddings):
        self.model = model
        self.embeddings = embeddings

        # Output Configuration
        structured_output = self.model.with_structured_output(RiskAssessmentEvalOutputV3)

        # Retrieval
        reference_retriever = self.faiss_retrieval(file_name="faiss_K+S+O_Train_v7")
        
        # Prompt
        self.prompt = "pi_rating_test_no_guitar_w_reference_v1"
        def make_template(data):
            _prompt = [
                ("system", self.prompt["system"]),
                ("user", self.prompt["user"].format(
                    process_major_category=data["process_major_category"],
                    process_sub_category=data["process_sub_category"],
                    equipment= data["equipment"],
                    material= data["material"],
                    hazard= data["hazard"],
                    reference=data["reference"],
                    mitigation= data["mitigation"],
                ))
            ]
            prompt_template = self.template_call("chat", _prompt)
            logger.debug(f"🔹 {_prompt = }")
            logger.debug(f"🔹 {prompt_template = }")
            return prompt_template

        # Reference Retriever
        reference_chain = (
            RunnablePassthrough()
            | self.get_dict2str(mapping=risk_assessment_map)
            | self.printer
            | reference_retriever
            | self.format_docs
        )

        # Input Configuration
        chain_init = self.parallel_init({
            "process_major_category": lambda x: x["process_major_category"],
            "process_sub_category": lambda x: x["process_sub_category"],
            "equipment":  lambda x: x["equipment"],
            "material":   lambda x: x["material"],
            "hazard": lambda x: x["hazard"],
            "mitigation": lambda x: x["mitigation"],
            "reference": reference_chain
        })

        # Final Prompt Chain
        prompt_chain = lambda x: make_template(x) | RunnablePassthrough()

        # Final Chain
        chain = chain_init | self.printer | prompt_chain | self.printer | structured_output | self.printer
        return chain
    
    def _register_chain(self, **kwargs):
        incorporation = kwargs.get("incorporation")
        model = kwargs.get("model")
        embeddings = kwargs.get("embeddings")

        logger.debug(f"🔹 {incorporation = }, {model = }, {embeddings = }")

        untag = lambda x: x.split(":")[0] if ":" in x else x
        
        self.chain = {
            "chain": self.chain_call(
                model=f"{incorporation}/{model}",
                embeddings=f"{incorporation}/{embeddings}"
            ),
            "path": f"/{untag(model)}/pi-ratings/eval/monarch/rag",
            "input_type": RiskAssessmentEvalInputV2,
            "output_type": RiskAssessmentEvalOutputV3
        }
        
        

__all__ = ["ProbabilityImpactRatingTestMonarchRAG"]
