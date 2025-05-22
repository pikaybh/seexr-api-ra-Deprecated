from schemas import ChecklistOutput
from models import ChainBase
from utils import get_logger

logger = get_logger(__name__)


def merge_process_category(data):
    if data["공종"] and data["공정"]:
        return f"{data['공종']} - {data['공정']}"
    elif data["공종"]:
        return data['공종']
    else:
        raise ValueError("`공종` is required.")



class CheckListV1(ChainBase):
    def chain_call(self, model, embeddings):
        self.model = model
        self.embeddings = embeddings

        # Prompt
        self.prompt = "checklist"
        prompt_template = self.template_call("chat", [
            ("system", self.prompt["system"]),
            ("user", self.prompt["user"].format(
                process_category="{process_category}",
                risk_assessment_table="{risk_assessment_table}",
            ))
        ])

        # Output Configuration
        structured_output = self.model.with_structured_output(ChecklistOutput)
        
        # Input Configuration
        chain_init = self.parallel_init({
            "process_category": lambda x: merge_process_category(x),
            "risk_assessment_table": lambda x: x["위험성평가표"],
        })

        # Final Chain
        chain = chain_init | self.printer | prompt_template | self.printer | structured_output | self.printer
        return chain
    
    def _register_chain(self, **kwargs):
        incorporation = kwargs.get("incorporation")
        model = kwargs.get("model")
        embeddings = kwargs.get("embeddings")

        self.chain = {
            "chain": self.chain_call(
                model=f"{incorporation}/{model}",
                embeddings=f"{incorporation}/{embeddings}"
            ),
            "path": f"/{model}/checklist",
            "input_type": ChecklistOutput,
        }

__all__ = ["CheckListV1"]


if __name__ == "__main__":
    from utils import pretty_print_risk_evaluation

    result = CheckListV1().chain_call(
        model="openai/gpt-4o",
        embeddings="openai/text-embedding-ada-002"
    ).invoke({
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
