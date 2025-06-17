"""250515_위험성평가 체인"""

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnablePassthrough

from schemas import RiskAssessmentInput, RiskAssessmentOutput, risk_assessment_map
from models import ChainBase
from utils import get_logger, print_return


logger = get_logger(__name__)



class ProbabilityImpactRatingV1(ChainBase):
    def chain_call(self, model, embeddings):
        self.model = model
        self.embeddings = embeddings

        # Output Configuration
        structured_output = self.model.with_structured_output(RiskAssessmentOutput)

        # Retrieval
        reference_retriever = self.faiss_retrieval(file_name="faiss_K+S+O_Openai_v3")
        
        # Prompt
        self.prompt = "cy_rma_v4"
        def make_template(data):
            _prompt = [
                ("system", self.prompt["system"]),
                ("user", self.prompt["user"].format(
                    process_major_category=data["process_major_category"],
                    process_sub_category=data["process_sub_category"],
                    equipment= data["equipment"],
                    material= data["material"],
                    task_description= data["task_description"],
                    # count=data["count"],
                    reference=data["reference"],
                ))
            ]
            for _image in data["site_image"]:
                _prompt.append(
                    HumanMessage(
                        content=[
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": _image
                                },
                            }
                        ]
                    )
                )
            prompt_template = self.template_call("chat", _prompt)
            logger.debug(f"🔹 {_prompt = }")
            logger.debug(f"🔹 {prompt_template = }")
            return prompt_template
        
        def find_risks_from_image(images):
            _prompt = [
                ("system", "사진에서 유해 위험요인을 **한국어**로 식별하십시오. 사진이 없다면 '사진 없음'이라고 답하십시오."),
            ]
            for _image in images:
                _prompt.append(
                    HumanMessage(
                        content=[
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": _image
                                },
                            }
                        ]
                    )
                )
            retriever_prompt = self.template_call("chat", _prompt)
            logger.debug(f"🔹 {_prompt = }")
            logger.debug(f"🔹 {retriever_prompt = }")
            return retriever_prompt

        from typing import List
        from pydantic import BaseModel, Field
        class RetrievalOutput(BaseModel):
            risk_items: List[str] = Field(description="사진 속 위험요인 목록")
        
        def call_merge_risks():
            @print_return
            def merge_risks(args: RetrievalOutput):
                merged_risks = "\n- ".join(args.risk_items)
                logger.debug(f"🔹 merge_risks: {args = }, {merged_risks = }")
                return merged_risks
            return merge_risks

        def call_merge_dicts_as_str():
            @print_return
            def merge_dicts_as_str(kwargs):
                logger.debug(f"🔹 merge_dicts_as_str: {kwargs = }")
                return "\n".join([f"{k}: {v}" for k, v in kwargs.items()])
            return merge_dicts_as_str

        # Identify Risks from Image
        from_image_chain = (
            lambda x: find_risks_from_image(x["site_image"]) 
            | RunnablePassthrough() 
            | self.printer 
            | self.model.with_structured_output(RetrievalOutput) 
            | self.printer 
            | call_merge_risks()
        )

        # Reference Retriever
        reference_chain_head = self.parallel_init({
            "위험 요인": from_image_chain,
            "작업 정보": self.get_dict2str(mapping=risk_assessment_map),
        })
        reference_chain_tail = (
            self.printer
            | RunnablePassthrough()
            | call_merge_dicts_as_str()
            | self.printer
            | reference_retriever
            | self.format_docs
        )
        reference_chain = reference_chain_head | reference_chain_tail

        # Input Configuration
        chain_init = self.parallel_init({
            "site_image": lambda x: x["site_image"],
            "process_major_category": lambda x: x["process_major_category"],
            "process_sub_category": lambda x: x["process_sub_category"],
            "equipment":  lambda x: x["equipment"],
            "material":   lambda x: x["material"],
            "task_description": lambda x: x["task_description"],
            # "count":      lambda x: x["count"],
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
            "path": f"/{untag(model)}/pi-ratings",
            "input_type": RiskAssessmentInput,
        }
        
        

__all__ = ["ProbabilityImpactRatingV1"]


if __name__ == "__main__":
    from utils import pretty_print_risk_evaluation_v2

    result = ProbabilityImpactRatingV1().chain_call(
        model="openai/gpt-4o",
        embeddings="openai/text-embedding-ada-002"
    ).invoke(
        {
    "process_major_category": "갱폼 작업",
    "process_sub_category": "갱폼 해체 및 반출",
    "equipment": "타워크레인",
    "material": "자재",
    "task_description": "콘크리트 타설 및 양생이 완료된 구조물 외벽부의 갱폼(Form System) 해체 및 자재 반출 작업이 계획되어 있다. 해당 작업은 타설된 구조물이 충분한 강도를 확보한 이후에 수행되며, 고정 상태의 갱폼을 분해하고, 타워크레인을 이용해 지정 장소로 안전하게 인양 및 적치하는 절차로 구성된다. 해체 대상 갱폼은 전일 타설 완료된 외벽 구간이며, 해체 시에는 상단 고정 클램프 해제 → 측면 패널 분리 → 프레임 분해 순으로 작업이 진행된다. 인양 장비로는 타워크레인 1대가 사용되며, 작업팀은 작업반장 1인, 해체공 3인, 신호수 1인의 5인 1조로 운영된다. 해체된 갱폼 자재는 현장 내 임시 적치장으로 운반된 후 재조립 또는 외부 반출을 위한 정비작업을 대기하게 되며, 자재의 상태에 따라 분류작업도 병행될 예정이다. 금일 작업은 특히 고층 작업 구간에서 진행되므로, 인양 중 낙하 및 충돌 방지를 위한 자재 결속 상태 확인과 하부 작업구역의 접근 통제가 철저히 관리되어야 한다. 자재 해체 시에는 작업 순서를 준수하며, 구조물 손상 방지를 위한 주의가 요구된다.",
    "site_image": ["https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAxNzEyMDRfMTY5%2FMDAxNTEyMzQ4MjU1NjM5.VNvxQPjcaguM96uoEyUB4NxDfUe5gQ4jHezEJoWzPg8g.bjU5NODTWlrDt0Xljtqok5_pZe3fUChlNcjcWo06AI8g.JPEG.tinki8%2F%25BD%25BD%25B6%25F3%25C0%25CC%25B5%25E54.JPG&type=sc960_832"],
    "count": "10"
  }
    )

    for k, v in dict(result).items():
        if k.strip().startswith("위험성평가표"):
            logger.info(f"- {k}:")
            for i in v:
                logger.info(f"  - {i}")
        else:
            logger.info(f"- {k}: {v}")

    pretty_print_risk_evaluation_v2(result.공종, 
                                    result.공정, 
                                    result.작업명, 
                                    result.위험성평가표, 
                                    result.기타)
