from typing import List, Literal
from pydantic import BaseModel, Field


class ProcessCategory(BaseModel):
    process_main_category: Literal["공통공사", "교량공사", "터널공사"] = Field(
        description="작업 공정 공사종류별 분류",
        examples=["공통공사", "교량공사", "터널공사"]
    )
    process_major_category: str = Field(
        description="작업 공정 대분류",
        examples=["거푸집작업", "가설 작업", "굴착작업"]
    )
    process_sub_category: str = Field(
        description="작업 공정 세부공정",
        examples=["갱폼 조립", "갱폼 자재반입", "가설도로 벌목 및 표토제거"]
    )


class Equipment(BaseModel):
    equipment: str = Field(
        description="설비 명칭",
        examples=["PSC빔", "SHIELD머신", "크레인", "굴삭기", "덤프트럭"]
    )

class Material(BaseModel):
    material: str = Field(
        description="물질 명칭",
        examples=["콘크리트", "철근", "가스", "갈탄", "분진"]
    )


class InputSheets(BaseModel):
    process_mapping: List[ProcessCategory] = Field(description="작업 공정 분류 정보")
    equipment_list: List[Equipment] = Field(description="설비 목록")
    material_list: List[Material] = Field(description="물질 목록")

__all__ = [
    "ProcessCategory",
    "Equipment",
    "Material",
    "InputSheets"
]
