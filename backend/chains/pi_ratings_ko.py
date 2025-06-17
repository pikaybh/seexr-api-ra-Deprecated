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
    ).invoke({
        "process_major_category": "기초파일작업",
        "process_sub_category": "기초파일 자재, 장비반입, 운반, 보관",
        "equipment": "지게차",
        "material": "",
        "task_description": "초공사 단계의 진행에 따라 기초파일 반입 및 적치작업, 파일 선행 정렬, 파일 박기 준비작업이 순차적으로 진행될 예정입니다. 오전 중에는 기초파일 자재가 현장으로 추가 반입되며, 트레일러 2대 분량의 파일이 도착 예정입니다. 해당 자재는 5톤 지게차를 이용하여 하차 후 지정된 파일 적치장소로 운반 및 정리하게 되며, 지게차 운전원 1명과 보조인력 2명이 투입됩니다.
        파일 반입 및 정리작업이 완료된 이후, 오후에는 박기작업을 위한 파일 정렬 및 위치 표시 작업이 진행됩니다. 측량팀 2인이 레벨기와 광파기를 활용하여 파일 중심 위치를 재확인하고, 마킹 및 수직도 기준선 설정을 완료할 예정입니다. 동시에, 현장 내 파일드라이버 설치작업이 진행되며, 80톤급 크롤러 크레인 1대를 사용하여 장비를 작업위치로 이동 및 세팅하게 됩니다. 크레인 운전원 1명과 장비 보조 2명, 작업감독자 1명이 배치됩니다.
        기초파일 박기 작업은 예비파일 3본에 대해 시험타입 형식으로 진행되며, 오후 중후반부터 시작하여 일몰 전까지 1~2본의 파일을 시공할 계획입니다. 타격은 디젤해머 방식으로 진행되며, 파일길이와 지반조건에 따라 관입저항 측정을 병행할 예정입니다. 파일 시공팀 4명이 투입되며, 파일 유지 및 수직도 확인을 위한 작업자가 별도로 배치됩니다.
        전반적으로 금일은 장비 및 자재의 정리, 시험타입을 중심으로 기초파일 공정의 초기단계를 집중적으로 수행하는 날로, 각 공정간 연계성과 장비 이동 효율성을 고려한 작업 배치가 중점적으로 이뤄질 예정입니다.",
        "site_image": ["https://lh6.googleusercontent.com/proxy/YQLmuoGq5msa3_sCnE5CNZRTP53MoQ9S_XnrzkxKHjJdZbhG4CqAHVzknEcw15x35pLc5dOD3AC0uaEDqiMFbJcY1OkNQ8jrVNW39BWR"],
        "count": "10"
    })

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
