from typing import Dict, List
from pydantic import BaseModel, Field

from .pi_rating import RiskItemV2


"""
checklist_map: Dict[str, str] = {
    "평가대상": "assessment_target",
    "위험성평가표": "risk_assessment_table",
    "체크리스트 항목": "checklists"
}
"""



class Checklist(RiskItemV2):
    체크리스트_항목: str = Field(description="체크리스트 항목")



class ChecklistOutput(BaseModel):
    평가대상: str = Field(description="평가 대상")
    체크리스트: List[Checklist] = Field(description="체크리스트 항목")


__all__ = [
    "Checklist",
    "ChecklistOutput",
]