from typing import Dict, List
from pydantic import BaseModel, Field


kras_map: Dict[str, str] = {
    "공종": "work_type",
    "공정": "procedure",
    "공정설명": "procedure_description",
    "설비": "equipment",
    "물질": "material",
    "유해위험요인_분류": "hazard_classification",
    "유해위험요인_원인": "hazard_cause",
    "유해위험요인": "hazard",
    "관련근거": "related_law",
    "위험_가능성": "risk_possibility",
    "위험_중대성": "risk_severity",
    "위험성": "risk_level",
    "감소대책": "risk_reduction_measures",
}



class KrasRiskAssessmentInput(BaseModel):
    work_type: str = Field(description="작업 공종의 이름")
    procedure: str = Field(description="작업 공정의 이름")

class KrasRiskMatrixAnalysisInput(BaseModel):
    image_path: List[str] = Field(description="현장 사진")
    count: int = Field(description="작업 횟수")
    work_type: str = Field(description="작업 공종의 이름")
    procedure: str = Field(description="작업 공정의 이름")

class KrasRiskMatrixAnalysisInputText(BaseModel):
    count: int = Field(description="작업 횟수")
    work_type: str = Field(description="작업 공종의 이름")
    procedure: str = Field(description="작업 공정의 이름")


class RiskItem(BaseModel):
    번호: int = Field(description="시리얼 숫자")
    공종: str = Field(description="작업 공종의 이름")
    공정: str = Field(description="작업 공정의 이름")
    공정설명: str = Field(description="작업 공정 설명")
    설비: str = Field(description="작업에 사용되는 설비 이름")
    물질: str = Field(description="작업 과정에서 취급되는 물질 이름")
    유해위험요인_분류: str = Field(description="유해 또는 위험 요인의 분류")
    유해위험요인_원인: str = Field(description="유해 또는 위험 요인의 발생 원인")
    유해위험요인: str = Field(description="유해 또는 위험 요인의 상세")
    관련근거: str = Field(description="관련된 근거 법령")
    위험_가능성: str = Field(description="위험이 발생할 가능성")
    위험_중대성: str = Field(description="위험이 미치는 영향의 심각성")
    위험성: str = Field(description="해당 위험 요소의 위험도")
    감소대책: List[str] | str = Field(description="위험 요소 감소를 위해 권장되는 통제 및 제한 조치 목록")




class KrasRiskAssessmentOutput(BaseModel):
    공종: str = Field(description="사용자가 입력한 공종의 이름")
    공정: str = Field(description="사용자가 입력한 공정의 이름")
    작업명: str = Field(description="사용자가 입력한 작업명")
    위험성평가표: List[RiskItem] = Field(description="각 위험 요소에 대한 위험성 평가와 통제 조치 목록")
    기타: List[str] = Field(description="기타 제언")


__all__ = ["KrasRiskAssessmentInput", "KrasRiskMatrixAnalysisInput", "KrasRiskMatrixAnalysisInputText", "KrasRiskAssessmentOutput", "kras_map"]
