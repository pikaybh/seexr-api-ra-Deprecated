from langserve import CustomUserType
from pydantic import Field

from typing import Dict, List
from pydantic import BaseModel, Field

#위험성평가 매핑
risk_assessment_map: Dict[str, str] = {
    # ── 입력 필드 ───────────────────
    "공정대분류": "process_major_category",
    "공정세부분류": "process_sub_category",
    "설비": "equipment",
    "물질": "material",
    "작업내용": "task_description",
    "이미지": "site_image",          # 현장사진

    # ── 출력 필드 ───────────────────
    "유해위험요인": "hazard",
    "사고분류": "accident_classification",
    "위험가능성": "risk_possibility",     # 빈도
    "위험중대성": "risk_severity",      # 강도
    "위험성": "risk",
    "감소대책": "risk_mitigation",
    "관련근거": "related_regulations",
}


class FileProcessingRequest(CustomUserType):
    """Request including a base64 encoded file."""

    # The extra field is used to specify a widget for the playground UI.
    file: str = Field("", extra={"widget": {"type": "base64file"}})
    num_chars: int = 100


# 위험성평가 자동화 모듈의 입력 필드
class RiskAssessmentInput(BaseModel):
    site_image: List[str] = Field(..., description="현장 사진")
    process_major_category: str = Field(description="작업 공정 대분류")
    process_sub_category: str = Field("", description="작업 공정 세부분류")
    equipment: str = Field("", description="작업에 사용되는 장비 및 설비")
    material: str = Field("", description="작업 과정에서 취급되는 물질 이름")
    task_description: str = Field("", description="현장 작업 내용")
    # count: int = Field(description="유해 위험요인 식별 개수")

# 위험성평가 자동화 모듈
class RiskItem(BaseModel):
    번호: int = Field(description="시리얼 숫자")
    공정대분류: str = Field(description="작업 공정 대분류")
    공정세부분류: str = Field(description="작업 공정 세부분류")
    설비: str = Field(description="작업에 사용되는 장비 및 설비")
    물질: str = Field(description="작업 과정에서 취급되는 물질")
    유해위험요인: str = Field(description="유해 또는 위험 요인")
    사고분류: str = Field(description="사고 분류")
    위험가능성: str = Field(description="위험이 발생하는 빈도")
    위험중대성: str = Field(description="위험이 미치는 영향의 심각성")
    위험성: str = Field(description="해당 위험 요소의 위험도")
    감소대책: str = Field(description="위험 요소 감소를 위해 권장되는 통제 및 조치")
    관련근거: str = Field(description="유해 위험요인에 따른 관련된 근거 법령")

class RiskItemV2(BaseModel):
    번호: int = Field(description="시리얼 숫자")
    공정대분류: str = Field(description="작업 공정 대분류")
    공정세부분류: str = Field(description="작업 공정 세부분류")
    유해위험요인: str = Field(description="유해 또는 위험 요인")
    사고분류: str = Field(description="사고 분류")
    위험가능성: str = Field(description="위험이 발생하는 빈도")
    위험중대성: str = Field(description="위험이 미치는 영향의 심각성")
    위험성: str = Field(description="해당 위험 요소의 위험도")
    감소대책: str = Field(description="위험 요소 감소를 위해 권장되는 통제 및 조치")
    관련근거: str = Field(description="유해 위험요인에 따른 관련된 근거 법령")



# 위험성평가 전체 output Framework
class RiskAssessmentOutput(BaseModel):
    공종: str = Field(description="사용자가 입력한 공종의 이름")
    공정: str = Field(description="사용자가 입력한 공정의 이름")
    작업명: str = Field(description="사용자가 입력한 작업명")
    위험성평가표: List[RiskItemV2] = Field(description="각 위험 요소에 대한 위험성 평가와 통제 조치 목록")
    기타: List[str] = Field(description="기타 제언")

__all__ = ["FileProcessingRequest", "RiskAssessmentInput", "RiskAssessmentOutput", "risk_assessment_map"]