"""250603_위험성평가 체인"""

from langchain_core.runnables import RunnablePassthrough

from schemas import RiskAssessmentEvalInput, RiskAssessmentEvalOutput
from models import ChainBase
from utils import get_logger


logger = get_logger(__name__)



class ProbabilityImpactRatingTestWoRAG(ChainBase):
    def chain_call(self, model, embeddings):
        self.model = model
        self.embeddings = embeddings

        # Output Configuration
        structured_output = self.model.with_structured_output(RiskAssessmentEvalOutput)
       
        # Prompt
        self.prompt = "pi_rating_test_wo_reference"
        def make_template(data):
            _prompt = [
                ("system", self.prompt["system"]),
                ("user", self.prompt["user"].format(
                    process_major_category=data["process_major_category"],
                    process_sub_category=data["process_sub_category"],
                    equipment= data["equipment"],
                    material= data["material"],
                    hazard= data["hazard"],
                ))
            ]
            prompt_template = self.template_call("chat", _prompt)
            logger.debug(f"🔹 {_prompt = }")
            logger.debug(f"🔹 {prompt_template = }")
            return prompt_template

        # Input Configuration
        chain_init = self.parallel_init({
            "process_major_category": lambda x: x["process_major_category"],
            "process_sub_category": lambda x: x["process_sub_category"],
            "equipment":  lambda x: x["equipment"],
            "material":   lambda x: x["material"],
            "hazard": lambda x: x["hazard"],
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
            "path": f"/{untag(model)}/pi-ratings/eval-wo-rag",
            "input_type": RiskAssessmentEvalInput,
            "output_type": RiskAssessmentEvalOutput
        }
        
        

__all__ = ["ProbabilityImpactRatingTestWoRAG"]
