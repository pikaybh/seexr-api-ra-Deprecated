"""250515_위험성평가 체인"""


from langchain_core.runnables import RunnablePassthrough

from structures import RiskAssessmentOutput, risk_assessment_map
from models import ChainBase
from utils import get_logger, print_return

logger = get_logger(__name__)



class RMAv2BY(ChainBase):
    def chain_call(self, model, embeddings):
        self.model = model
        self.embeddings = embeddings

        # Output Configuration
        structured_output = self.model.with_structured_output(RiskAssessmentOutput)

        # Retrieval
        reference_retriever = self.faiss_retrieval(file_name="faiss_K+S+O_o_v2")
        
        from langchain_core.messages import HumanMessage
        # Prompt
        self.prompt = "cy_rma_v3"
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
            for image in data["site_image"]:
                _prompt.append(
                    HumanMessage(
                        content=[
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image
                                },
                            }
                        ]
                    )
                )
            prompt_template = self.template_call("chat", _prompt)
            return prompt_template
        
        def find_risks_from_image(images):
            _prompt = [
                ("system", "사진에서 유해 위험요인을 식별하십시오. 사진이 없다면 '사진 없음'이라고 답하십시오."),
            ]
            for image in images:
                _prompt.append(
                    HumanMessage(
                        content=[
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image
                                },
                            }
                        ]
                    )
                )
            retriever_prompt = self.template_call("chat", _prompt)

            return retriever_prompt

        from typing import List
        from pydantic import BaseModel, Field
        class RetrievalOutput(BaseModel):
            risk_items: List[str] = Field(description="사진 속 위험요인 목록")
        
        @print_return
        def merge_risks(kwargs):
            return "\n- ".join(kwargs)

        from langchain_core.runnables import RunnableParallel, RunnableLambda

        def merge_dicts_as_str_shell():
            @print_return
            def merge_dicts_as_str(kwargs):
                print(f"merge_dicts_as_str: {kwargs = }")
                return "\n".join([f"{k}: {v}" for k, v in kwargs.items()])
            return merge_dicts_as_str

        # Input Configuration
        chain_init = self.parallel_init({
            # "site_image": lambda x: self.image_preprocessor(x.get("site_image", [])),
            "site_image": lambda x: x["site_image"],  # get_site_image | RunnableLambda(_process_file).with_types(input_type=FileProcessingRequest),
            "process_major_category": lambda x: x["process_major_category"],
            "process_sub_category": lambda x: x["process_sub_category"],
            "equipment":  lambda x: x["equipment"],
            "material":   lambda x: x["material"],
            "task_description": lambda x: x["task_description"],
            # "count":      lambda x: x["count"],
            "reference": self.parallel_init({
                "사진 속 위험요인 목록": lambda x: find_risks_from_image(x["site_image"]) | self.printer | self.model.with_structured_output(RetrievalOutput) | self.printer | merge_risks,
                "작업 정보": self.get_dict2str(mapping=risk_assessment_map),
            })
            | RunnablePassthrough()
            | merge_dicts_as_str_shell()
            | self.printer
            # | RunnablePassthrough()
            | reference_retriever
            | self.format_docs
        })

        # Final Chain
        chain = chain_init | self.printer | make_template | self.printer | structured_output | self.printer
        return chain

__all__ = ["RMAv2BY"]


if __name__ == "__main__":
    from utils import pretty_print_risk_evaluation

    result = RMAv2BY().chain_call(
        model="openai/gpt-4o",
        embeddings="openai/text-embedding-ada-002"
    ).invoke({
        "process": "토공작업",
        "subprocess": "",
        "equipment": "소형 크레인, 지게차, 굴삭기",
        "material": "토사",
        "workdetail": "금일 계획은 다음과 같습니다. 토공 작업으로는 리핑암 절취와 상차, 녹지대 성토, 외부 토사 반입 및 법면 절취가 포함되며, 구조물 공사로는 패널 및 블록 설치와 내부 거푸집 설치가 예정되어 있습니다. 부대공은 철거와 천공, 발파 작업이 있습니다.",
        "image_paths": [],
        "count": "10"
    })

    for k, v in dict(result).items():
        if k.strip().startswith("위험성평가표"):
            logger.info(f"- {k}:")
            for i in v:
                logger.info(f"  - {i}")
        else:
            logger.info(f"- {k}: {v}")

    pretty_print_risk_evaluation(
        result.공종, result.공정, result.작업명, result.위험성평가표, result.기타
    )
