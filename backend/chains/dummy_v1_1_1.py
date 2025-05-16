from langchain_core.runnables import RunnablePassthrough

from structures import RiskAssessmentOutput, risk_assessment_map
from utils import get_logger

logger = get_logger(__name__)

dummy_item = {
    "output": {
        "공종": "토공작업",
        "공정": "기타",
        "작업명": "리핑암 절취와 상차",
        "위험성평가표": [
        {
            "번호": 1,
            "공정대분류": "토공작업",
            "공정세부분류": "리핑암 절취",
            "설비": "소형 크레인",
            "물질": "토사",
            "유해위험요인": "작업 구간 접근방지 조치 미실시로 인한 협착 위험",
            "사고분류": "끼임",
            "위험가능성": "중",
            "위험중대성": "중",
            "위험성": "보통",
            "감소대책": "작업구간 출입통제 철저히 하고, 경광등과 후진 경보음 및 후방감시카메라 설치",
            "관련근거": "제20조(출입의 금지 등)"
        },
        {
            "번호": 2,
            "공정대분류": "토공작업",
            "공정세부분류": "상차",
            "설비": "지게차",
            "물질": "토사",
            "유해위험요인": "장비 분리작업 중 넘어진 지게차에 깔릴 위험",
            "사고분류": "깔림",
            "위험가능성": "중",
            "위험중대성": "상",
            "위험성": "높음",
            "감소대책": "장비 해체작업 시 해체작업 계획서 작성 및 전도방지 조치 수립",
            "관련근거": "제384조(해체작업 시 준수사항)"
        },
        {
            "번호": 3,
            "공정대분류": "토공작업",
            "공정세부분류": "녹지대 성토",
            "설비": "굴삭기",
            "물질": "토사",
            "유해위험요인": "굴삭기 작업 중 쏟아지는 흙에 깔림",
            "사고분류": "깔림",
            "위험가능성": "중",
            "위험중대성": "상",
            "위험성": "높음",
            "감소대책": "작업 시 주변 접근 금지 및 전도방지 조치 강화",
            "관련근거": "없음"
        },
        {
            "번호": 4,
            "공정대분류": "토공작업",
            "공정세부분류": "녹지대 성토",
            "설비": "굴삭기",
            "물질": "토사",
            "유해위험요인": "굴삭기 전도 시 위험",
            "사고분류": "넘어짐",
            "위험가능성": "중",
            "위험중대성": "상",
            "위험성": "높음",
            "감소대책": "지반 안전성 검토 및 장비 안정성 확보 수립",
            "관련근거": "없음"
        },
        {
            "번호": 5,
            "공정대분류": "토공작업",
            "공정세부분류": "외부 토사 반입",
            "설비": "소형 크레인",
            "물질": "토사",
            "유해위험요인": "크레인 전도 및 전복 위험",
            "사고분류": "넘어짐",
            "위험가능성": "중",
            "위험중대성": "상",
            "위험성": "높음",
            "감소대책": "작업 전 안정성 사전검토",
            "관련근거": "없음"
        },
        {
            "번호": 6,
            "공정대분류": "토공작업",
            "공정세부분류": "법면 절취",
            "설비": "굴삭기",
            "물질": "토사",
            "유해위험요인": "법면 붕괴로 인한 매몰 위험",
            "사고분류": "깔림",
            "위험가능성": "중",
            "위험중대성": "상",
            "위험성": "높음",
            "감소대책": "법면 안정성 평가 및 사전 보강",
            "관련근거": "없음"
        },
        {
            "번호": 7,
            "공정대분류": "구조물 공사",
            "공정세부분류": "패널 설치",
            "설비": "지게차",
            "물질": "토사",
            "유해위험요인": "무거운 패널의 미끄러짐으로 인한 부상",
            "사고분류": "부딪힘",
            "위험가능성": "중",
            "위험중대성": "중",
            "위험성": "보통",
            "감소대책": "작업구간 출입 통제 및 안전지주 사용",
            "관련근거": "제20조(출입의 금지 등)"
        },
        {
            "번호": 8,
            "공정대분류": "구조물 공사",
            "공정세부분류": "블록 설치",
            "설비": "소형 크레인",
            "물질": "토사",
            "유해위험요인": "블록 이동 시 근로자 협착 위험",
            "사고분류": "끼임",
            "위험가능성": "중",
            "위험중대성": "중",
            "위험성": "보통",
            "감소대책": "블록 이동시 후방감시카메라 설치 및 후진 경보음 의무적 사용",
            "관련근거": "제20조(출입의 금지 등)"
        },
        {
            "번호": 9,
            "공정대분류": "부대공",
            "공정세부분류": "철거",
            "설비": "소형 크레인",
            "물질": "토사",
            "유해위험요인": "철거 시 구조물 붕괴",
            "사고분류": "떨어짐(2미터 이상)",
            "위험가능성": "중",
            "위험중대성": "상",
            "위험성": "높음",
            "감소대책": "철거 계획서 작성 및 안전 조치 수립",
            "관련근거": "제384조(해체작업 시 준수사항)"
        },
        {
            "번호": 10,
            "공정대분류": "부대공",
            "공정세부분류": "발파",
            "설비": "굴삭기",
            "물질": "토사",
            "유해위험요인": "발파 작업 시 튀어나온 파편의 충돌",
            "사고분류": "물체에 맞음",
            "위험가능성": "중",
            "위험중대성": "상",
            "위험성": "높음",
            "감소대책": "작업 구간 접근 금지 및 안전 울타리 설치",
            "관련근거": "없음"
        }
        ],
        "기타": []
    },
    "metadata": {
        "run_id": "97acd4a2-af49-4cd8-8f66-da6a13e9b0ac",
        "feedback_tokens": []
    }
}

def chain_call(self, model, embeddings):
    self.model = model
    self.embeddings = embeddings

    # Output Configuration
    structured_output = self.model.with_structured_output(RiskAssessmentOutput)

    # Retrieval
    reference_retriever = self.faiss_retrieval(file_name="faiss_K+S+O_o_v2")

    # Prompt
    self.prompt = "cy_rma_v3"
    prompt_template = self.template_call("chat", [
        ("system", self.prompt["system"]),
        ("user", "{site_image}"),
        ("user", self.prompt["user"].format(
            process_major_category="{process_major_category}",
            process_sub_category="{process_sub_category}",
            equipment= "{equipment}",
            material= "{material}",
            task_description= "{task_description}",
            # count="{count}",
            reference="{reference}",
        ))
    ])

    # Input Configuration
    chain_init = self.parallel_init({
        "site_image": lambda x: self.image_preprocessor(x.get("site_image", [])),
        "process_major_category":    lambda x: x["process_major_category"],
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
    chain = chain_init | prompt_template | structured_output
    return chain

__all__ = ["dummy_item"]