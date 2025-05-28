from typing import List
from pydantic import BaseModel, Field

from .pi_rating import RiskItemV3


"""
checklist_map: Dict[str, str] = {
    "평가대상": "assessment_target",
    "위험성평가표": "risk_assessment_table",
    "체크리스트 항목": "checklists"
}
"""



class Checklist(RiskItemV3):
    체크리스트_항목: str = Field(
        description="체크리스트 항목. 각 위험 요소에 대한 체크리스트 항목으로, 해당 유해·위험 요인이 위험성 평가 대상에 적용되는지 여부를 확인하는 데 사용됩니다.",
    )



class ChecklistOutput(BaseModel):
    평가대상: str = Field(description="평가 대상")
    체크리스트: List[Checklist] = Field(description="체크리스트 항목을 포함한 위험성평가표 전체.")


__all__ = [
    "Checklist",
    "ChecklistOutput",
]