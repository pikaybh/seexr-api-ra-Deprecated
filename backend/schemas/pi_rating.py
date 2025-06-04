from typing import Dict, List, Literal

from langserve import CustomUserType
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


# 파일을 base64로 인코딩하여 전송하는 요청 형식
class FileProcessingRequest(CustomUserType):
    """
    Request including a base64 encoded file.
    The extra field is used to specify a widget for the playground UI.
    """
    file: str = Field("", extra={"widget": {"type": "base64file"}})
    num_chars: int = 100


# 위험성평가 자동화 모듈의 입력 필드
class RiskAssessmentInput(BaseModel):
    site_image: List[str] = Field(
        ..., 
        description="현장 사진들. 이미지 URL 혹은 base64로 encoding한 데이터 문자열. 사진이 없을 경우 빈 리스트(Array)를 입력하세요.",
        examples=[
            "https://example.com/image1.jpg",
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA...",
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
        ]
    )
    process_major_category: str = Field(
        description="작업 공정 대분류. 전체 건설 프로젝트 내 공사 흐름의 최상위 레벨 카테고리로, 유해·위험 요인을 공정별로 그룹화하거나 책임 단위를 분류할 때 기준이 됨.",
        examples=["토목", "건축", "기계설비", "전기", "조경", "안전관리"]
    )
    process_sub_category: str = Field(
        "", 
        description="작업 공정 세부분류. 대분류 아래의 세부적 작업 유형으로, 실제 위험요인이 발생하는 구체적 작업 상황을 명확하게 식별하는 데 사용됨.",
        examples=["기초공사", "골조공사", "마감공사", "설비공사", "전기공사"]
    )
    equipment: str = Field(
        "", 
        description="설비 및 장비. 작업에 사용되는 설비 및 장비.",
        examples=["크레인", "굴착기", "타워크레인", "지게차", "콘크리트 믹서"]
    )
    material: str = Field(
        "", 
        description="화학 및 인화 물질. 작업 과정에서 취급되는 화학 및 인화성 물질 이름",
        examples=["시멘트", "페인트", "휘발유", "가솔린", "화학약품"]
    )
    task_description: str = Field(
        "", 
        description="현장 작업 내용에 대한 설명 상세. “작업지시서”, “PTW” 등 작업 전 사전 서류를 긁어와서 사용하는 것을 의도함"
    )
    count: int = Field(10, description="(Deprecated) 유해 위험요인 식별 개수", deprecated=True)

# 위험성평가 자동화 모듈
class RiskItem(BaseModel):
    """
    [Deprecated] 위험성평가 자동화 모듈의 아이템 필드 V1. RiskItemV2를 사용하세요.
    """
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
    """
    [Deprecated] 위험성평가 자동화 모듈의 아이템 필드 V2. RiskItemV3를 사용하세요.
    """
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

class RiskItemV3(BaseModel):
    """
    위험성평가 자동화 모듈의 아이템 필드 V3
    """
    번호: int = Field(
        description="연번. 각 위험요인 항목을 식별하기 위한 연속적인 일련번호로, 보고서 상에서 해당 리스크 항목을 참조할 때 사용할 수 있음.",
        examples=[1, 2, 3, 4, 5]
    )
    공정대분류: str = Field(
        description="작업 공정 대분류. 전체 건설 프로젝트 내 공사 흐름의 최상위 레벨 카테고리로, 유해·위험 요인을 공정별로 그룹화하거나 책임 단위를 분류할 때 기준이 됨.",
        examples=["토목", "건축", "기계설비", "전기", "조경", "안전관리"]
    )
    공정세부분류: str = Field(
        description="작업 공정 세부분류. 대분류 아래의 세부적 작업 유형으로, 실제 위험요인이 발생하는 구체적 작업 상황을 명확하게 식별하는 데 사용됨.",
        examples=["기초공사", "골조공사", "마감공사", "설비공사", "전기공사"]
    )
    유해위험요인: str = Field(
        description="유해·위험 요인. 해당 공정·작업에서 실제로 잠재하거나 표면화된 유해성·위험성을 구체적으로 기재. 위험성평가(정성/정량) 과정의 중심이 되는 필드.",
    )
    사고분류: Literal[
        '감전', '기타', '깔림', '끼임', '넘어짐', '떨어짐', '물체에 맞음', '부딪힘', '절단 및 베임', '질병', '질식', '찔림', '화상'
    ] = Field(
        description="사고 분류. 해당 위험요인으로 인해 실제 또는 잠재적으로 발생 가능한 사고의 유형을 표준화된 분류 체계에 따라 기록함.",
        examples=[
            '감전', '기타', '깔림', '끼임', '넘어짐', '떨어짐', '물체에 맞음', '부딪힘', '절단 및 베임', '질병', '질식', '찔림', '화상'
        ]
    )
    위험가능성: Literal["낮음(1)", "중간(2)", "높음(3)"] = Field(
        description="위험이 발생하는 빈도. 해당 위험요인이 건설 현장에서 어느 정도 자주 노출·발생하는지에 대한 정성적 또는 정량적 평가. 현장 실태와 과거 사례, 데이터 기반으로 평가할 것.",
        examples=["낮음(1)", "중간(2)", "높음(3)"]
    )
    위험중대성: Literal["낮음(1)", "중간(2)", "높음(3)"] = Field(
        description="위험이 미치는 영향의 심각성. 위험요인이 현실화될 경우 인적·물적·법적 측면에서 초래할 수 있는 결과의 심각도(예: 치명상, 다수 피해, 경상, 경미 손실 등)로, 안전관리에서 우선순위 결정에 핵심적 기준이 됨.",
        examples=["낮음(1)", "중간(2)", "높음(3)"]
    )
    위험성: Literal["낮음(1)", "낮음(2)", "중간(3)", "중간(4)", "높음(6)", "높음(9)"] = Field(
        description="해당 유해·위험 요인의 위험성. '위험가능성'과 '위험중대성'의 조합 또는 정량적 산식('위험가능성'×'위험중대성')에 따라 평가된 총체적 위험수준. 대응·관리 우선순위 결정에 활용.",
        examples=["낮음(1)", "낮음(2)", "중간(3)", "중간(4)", "높음(6)", "높음(9)"]
    )
    감소대책: str = Field(
        description="위험 감소대책. 위험 감소를 위해 권장되는 통제 및 조치. 해당 위험요인을 저감 또는 제거하기 위한 구체적 관리방안, 예방조치, 공법, 교육·훈련, 보호구 지급 등 실질적 조치사항을 기술.",
        examples=["안전난간 설치", "작업자 교육", "보호구 지급", "위험 표지판 설치", "정기 점검"]
    )
    관련근거: str = Field(
        description="법적 근거. 유해·위험 요인에 따른 관련된 근거 법령. 해당 위험요인 및 감소대책의 법적·제도적 근거 등의 명칭과 조문을 기재.",
        examples=["산업안전보건법 제23조", "KOSHA Guide 2019", "건설기계 안전관리 규정"]
    )


# 위험성평가 전체 output Framework
class RiskAssessmentOutput(BaseModel):
    공종: str = Field(
        description="작업 공정 대분류. 사용자가 입력한 작업 공정 대분류"
    )
    공정: str = Field(
        description="작업 공정 세부분류. 사용자가 입력한 대분류 아래의 세부적 작업 유형"
    )
    작업명: str = Field(description="(Deprecated) 사용자가 입력한 작업명", deprecated=True)
    위험성평가표: List[RiskItemV3] = Field(
        description="위험성평가표 아이템. 각 위험 요소에 대한 위험성 평가와 통제 조치 목록"
    )
    기타: List[str] = Field(
        description="기타 제언. 위험성평가표에 포함되지 않는 추가적인 제언이나 주의사항을 기술"
    )



# 위험성평가 자동화 실험을 위한 모듈 의 입력 필드
class RiskAssessmentEvalInput(BaseModel):
    process_major_category: str = Field(
        description="작업 공정 대분류. 전체 건설 프로젝트 내 공사 흐름의 최상위 레벨 카테고리로, 유해·위험 요인을 공정별로 그룹화하거나 책임 단위를 분류할 때 기준이 됨.",
        examples=["토목", "건축", "기계설비", "전기", "조경", "안전관리"]
    )
    process_sub_category: str = Field(
        "", 
        description="작업 공정 세부분류. 대분류 아래의 세부적 작업 유형으로, 실제 위험요인이 발생하는 구체적 작업 상황을 명확하게 식별하는 데 사용됨.",
        examples=["기초공사", "골조공사", "마감공사", "설비공사", "전기공사"]
    )
    equipment: str = Field(
        "", 
        description="설비 및 장비. 작업에 사용되는 설비 및 장비.",
        examples=["크레인", "굴착기", "타워크레인", "지게차", "콘크리트 믹서"]
    )
    material: str = Field(
        "", 
        description="화학 및 인화 물질. 작업 과정에서 취급되는 화학 및 인화성 물질 이름",
        examples=["시멘트", "페인트", "휘발유", "가솔린", "화학약품"]
    )
    hazard: str = Field(
        "", 
        description="유해위험요인. 위험성 평가를 위해 식별된 유해 또는 위험 요인",
    )
    count: int = Field(10, description="(Deprecated) 유해 위험요인 식별 개수", deprecated=True)

__all__ = ["FileProcessingRequest", "RiskAssessmentInput", "RiskAssessmentOutput", "risk_assessment_map",
           "RiskAssessmentEvalInput"]