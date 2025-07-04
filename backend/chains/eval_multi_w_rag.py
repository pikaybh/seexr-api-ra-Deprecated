"""250603_위험성평가 체인"""

from langchain_core.runnables import RunnablePassthrough

from schemas import RiskAssessmentEvalInputV2, RiskAssessmentOutput, risk_assessment_map  # , MultiLabelAccidentClassificationOutputV2
from models import ChainBase
from utils import get_logger


logger = get_logger(__name__)


class EvalMultiRAG(ChainBase):
    _ds_num: int

    def __init__(self, ds_num: int):
        super().__init__()
        self.ds_num = ds_num

    @property
    def ds_num(self) -> int:
        return self._ds_num
    
    @ds_num.setter
    def ds_num(self, value: int):
        self._ds_num = value

    def chain_call(self, model, embeddings):
        self.model = model
        self.embeddings = embeddings

        # Output Configuration
        structured_output = self.model.with_structured_output(RiskAssessmentOutput)

        # Retrieval
        reference_retriever = self.faiss_retrieval(file_name=f"faiss_K+S+O_Train_v7_{self.ds_num}")
        
        # Prompt
        self.prompt = "pi_rating_test_w_reference_v4"
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
            | reference_retriever
            | self.format_table
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
        chain = chain_init | prompt_chain | structured_output | self.printer
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
            "path": f"/{untag(model)}/eval/multi-label/rag/{self.ds_num}",
            "input_type": RiskAssessmentEvalInputV2,
            "output_type": RiskAssessmentOutput
        }



__all__ = [f"EvalMultiRAG"]
