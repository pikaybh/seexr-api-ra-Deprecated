"""250515_위험성평가 체인"""


import base64
from langchain_core.document_loaders import Blob
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.document_loaders.parsers.images import BaseImageBlobParser

from structures import FileProcessingRequest, RiskAssessmentOutput, risk_assessment_map
from models import ChainBase
from utils import get_logger

logger = get_logger(__name__)


class ImageBlobParser(BaseImageBlobParser):
    def _analyze_image(self, img) -> str:
        import io

        image_bytes = io.BytesIO()
        img.save(image_bytes, format="PNG")
        img_base64 = base64.b64encode(image_bytes.getvalue()).decode("utf-8")

        return f"data:image/jpeg;base64,{img_base64}"



def get_site_image(data) -> str:
    """Get the site image from the request."""
    return data["site_image"]


def _process_file(request: FileProcessingRequest) -> str:
    """Extract the text from the first page of the PDF."""
    content = base64.b64decode(request.file.encode("utf-8"))
    blob = Blob(data=content)
    return ImageBlobParser().lazy_parse(blob)


def is_site_image(data) -> str:
    """Check if the data is an image."""
    f = data["site_image"]
    return bool(list(f))




"""
    content = base64.b64decode(request["site_image"].file.encode("utf-8"))
    blob = Blob(data=content)

    documents = list(BaseImageBlobParser().lazy_parse(blob))
    content = documents[0].page_content
    return content[: request.num_chars]

        image_bytes = io.BytesIO()
        img.save(image_bytes, format="PNG")
        img_base64 = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
        msg = self.model.invoke(
            [
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": self.prompt.format(format=format),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"
                            },
                        },
                    ]
                )
            ]
        )
"""


class RMAv2CY(ChainBase):
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
            if data["site_image"]:

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
            return ( RunnablePassthrough() | prompt_template )

        """
        prompt_template = self.template_call("chat", [
            ("system", self.prompt["system"]),
            ("user", self.prompt["user"].format(
                process_major_category="{process_major_category}",
                process_sub_category="{process_sub_category}",
                equipment= "{equipment}",
                material= "{material}",
                task_description= "{task_description}",
                # count="{count}",
                reference="{reference}",
            ))].append(
                HumanMessage(
                    content=[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image
                            },
                        }
                    ]
                ) for image in "{site_image}" if image
            )
        )
        """

        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.messages import HumanMessage, SystemMessage

        neo_prompt = ChatPromptTemplate(
            [
                SystemMessage(
                    content=[
                        {
                            "type": "text",
                            "text": self.prompt["system"],
                        }
                    ],
                ),
                HumanMessage(
                    content=[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "{site_image}"
                            },
                        }
                    ]
                ),
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": self.prompt["user"].format(
                                process_major_category="{process_major_category}",
                                process_sub_category="{process_sub_category}",
                                equipment= "{equipment}",
                                material= "{material}",
                                task_description= "{task_description}",
                                # count="{count}",
                                reference="{reference}",
                            )
                        }
                    ]
                )
            ]
        )

        """
        def is_image(data):
            " ""Check if the data is an image."  ""
            return neo_prompt if is_site_image(data) else prompt_template
        """

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
            "reference": (
                self.get_dict2str(mapping=risk_assessment_map)
                | RunnablePassthrough()
                | reference_retriever
                | self.format_docs
            ),
        })

        # Final Chain
        chain = chain_init | self.printer | make_template | self.printer | structured_output | self.printer
        return chain

__all__ = ["RMAv2"]


if __name__ == "__main__":
    from utils import pretty_print_risk_evaluation

    result = RMAv2CY().chain_call(
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

__all__ = ["RMAv2CY"]