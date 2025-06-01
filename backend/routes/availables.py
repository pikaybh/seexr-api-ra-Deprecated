from typing import List, Literal, Optional

from fastapi import Query, HTTPException

from models import BaseRouter
from schemas import (Provider,
                     EnumProviderAlias,
                     Providers,
                     LargeLanguageModel,
                     ProcessCategory, 
                     Equipment, 
                     Material, 
                     InputSheets)

language_models = Providers(
    items=[
        Provider(
            name="OpenAI",
            alias="openai",
            models=[
                LargeLanguageModel(name="gpt-4", type="chat", available=True),
                LargeLanguageModel(name="gpt-4o-mini", type="chat", available=True),
                LargeLanguageModel(name="text-embedding-ada-002", type="embedding", available=True),
            ]
        ),
        Provider(
            name="DeepSeek",
            alias="ds",
            models=[
                LargeLanguageModel(name="deepseek-r1:32b", type="chat", available=False),
            ]
        ),
        Provider(
            name="LG AI",
            alias="lgai",
            models=[
                LargeLanguageModel(name="exaone3.5:latest", type="chat", available=False),
            ]
        )
    ]
)

input_sheets = InputSheets(
    process_mapping=[
        ProcessCategory(process_main_category="공통공사", process_major_category="거푸집작업", process_sub_category="갱폼 조립"),
        ProcessCategory(process_main_category="공통공사", process_major_category="거푸집작업", process_sub_category="갱폼 자재반입"),
        ProcessCategory(process_main_category="공통공사", process_major_category="가설 작업", process_sub_category="가설도로 벌목 및 표토제거"),
        ProcessCategory(process_main_category="공통공사", process_major_category="가설 작업", process_sub_category="가설도로 시공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="가설 작업", process_sub_category="분전반 설치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="가설 작업", process_sub_category="이동식전기기계기구 방호조치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="가설 작업", process_sub_category="접지 설치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="가설 작업", process_sub_category="충전부 방호조치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="가설 작업", process_sub_category="가체철(물막이) 흙막이 시공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="가설 작업", process_sub_category="가제철(물막이) 장비반입"),
        ProcessCategory(process_main_category="공통공사", process_major_category="거푸집작업", process_sub_category="갱폼 인양, 설치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="거푸집작업", process_sub_category="갱폼 해체, 반출"),
        ProcessCategory(process_main_category="공통공사", process_major_category="거푸집작업", process_sub_category="거푸집 동바리 인양"),
        ProcessCategory(process_main_category="공통공사", process_major_category="거푸집작업", process_sub_category="거푸집 동바리 해체"),
        ProcessCategory(process_main_category="공통공사", process_major_category="거푸집작업", process_sub_category="자재반입, 가공·운반"),
        ProcessCategory(process_main_category="공통공사", process_major_category="거푸집작업", process_sub_category="거푸집 동바리 조립"),
        ProcessCategory(process_main_category="공통공사", process_major_category="굴착작업", process_sub_category="굴착 토사반출"),
        ProcessCategory(process_main_category="공통공사", process_major_category="굴착작업", process_sub_category="굴착 "),
        ProcessCategory(process_main_category="공통공사", process_major_category="굴착작업", process_sub_category="굴착 장비반입"),
        ProcessCategory(process_main_category="공통공사", process_major_category="그라우팅 작업", process_sub_category="그라우팅 천공 및 시공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="그라우팅 작업", process_sub_category="그라우팅 장비 및 자재반입"),
        ProcessCategory(process_main_category="공통공사", process_major_category="금속 및 잡철물 시공", process_sub_category="자재반입, 가공, 운반"),
        ProcessCategory(process_main_category="공통공사", process_major_category="금속 및 잡철물 시공", process_sub_category="금속 및 잡철물 시공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="기계설비 작업", process_sub_category="기계설비 설치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="기계설비 작업", process_sub_category="기계설비, 자재반입, 가공, 운반"),
        ProcessCategory(process_main_category="공통공사", process_major_category="기초파일작업", process_sub_category="기초파일 항타"),
        ProcessCategory(process_main_category="공통공사", process_major_category="기초파일작업", process_sub_category="기초파일 천공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="기초파일작업", process_sub_category="기초파일 자재, 장비반입, 운반, 보관"),
        ProcessCategory(process_main_category="공통공사", process_major_category="기초파일작업", process_sub_category="기초파일 두부정리"),
        ProcessCategory(process_main_category="공통공사", process_major_category="도장작업", process_sub_category="실내도장"),
        ProcessCategory(process_main_category="공통공사", process_major_category="도장작업", process_sub_category="실외도장"),
        ProcessCategory(process_main_category="공통공사", process_major_category="도장작업", process_sub_category="면처리"),
        ProcessCategory(process_main_category="공통공사", process_major_category="되메움 작업", process_sub_category="토사반입 및 되메움실시"),
        ProcessCategory(process_main_category="공통공사", process_major_category="되메움 작업", process_sub_category="토사다짐"),
        ProcessCategory(process_main_category="공통공사", process_major_category="맨홀 및 관 부설 작업", process_sub_category="맨홀 및 관 부설"),
        ProcessCategory(process_main_category="공통공사", process_major_category="맨홀 및 관 부설 작업", process_sub_category="맨홀 및 관 부설 굴착"),
        ProcessCategory(process_main_category="공통공사", process_major_category="발파작업", process_sub_category="발파 장약"),
        ProcessCategory(process_main_category="공통공사", process_major_category="발파작업", process_sub_category="발파"),
        ProcessCategory(process_main_category="공통공사", process_major_category="발파작업", process_sub_category="발파 천공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="발파작업", process_sub_category="발파 암처리"),
        ProcessCategory(process_main_category="공통공사", process_major_category="발파작업", process_sub_category="발파 화약고 관리"),
        ProcessCategory(process_main_category="공통공사", process_major_category="방수작업", process_sub_category="방수면처리, 방수 및 보호몰탈 등 시공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="부대토목 작업", process_sub_category="부대토목 옹벽시공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="부대토목 작업", process_sub_category="부대토목 구내 포장"),
        ProcessCategory(process_main_category="공통공사", process_major_category="석재 및 타일 작업", process_sub_category="자재반입, 운반"),
        ProcessCategory(process_main_category="공통공사", process_major_category="석재 및 타일 작업", process_sub_category="석재 및 타일 붙임"),
        ProcessCategory(process_main_category="공통공사", process_major_category="석재 및 타일 작업", process_sub_category="타일줄눈, 코킹시공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="수장 작업", process_sub_category="수장 시공(석고보드, 도배 등)"),
        ProcessCategory(process_main_category="공통공사", process_major_category="수장 작업", process_sub_category="수장 자재반입, 운반"),
        ProcessCategory(process_main_category="공통공사", process_major_category="수직구 작업", process_sub_category="수직구 흙막이 지보공 시공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="수직구 작업", process_sub_category="수직구 굴착"),
        ProcessCategory(process_main_category="공통공사", process_major_category="수직구 작업", process_sub_category="수직구 토사반출"),
        ProcessCategory(process_main_category="공통공사", process_major_category="수직구 작업", process_sub_category="수직구 보강"),
        ProcessCategory(process_main_category="공통공사", process_major_category="거푸집작업", process_sub_category="슬립폼 인양"),
        ProcessCategory(process_main_category="공통공사", process_major_category="거푸집작업", process_sub_category="슬립폼 해체"),
        ProcessCategory(process_main_category="공통공사", process_major_category="거푸집작업", process_sub_category="슬립폼 제작"),
        ProcessCategory(process_main_category="공통공사", process_major_category="안전가시설 작업", process_sub_category="가설통로 또는 가설계단"),
        ProcessCategory(process_main_category="공통공사", process_major_category="안전가시설 작업", process_sub_category="비계"),
        ProcessCategory(process_main_category="공통공사", process_major_category="안전가시설 작업", process_sub_category="개구부"),
        ProcessCategory(process_main_category="공통공사", process_major_category="안전가시설 작업", process_sub_category="작업발판"),
        ProcessCategory(process_main_category="공통공사", process_major_category="엘리베이터 설치작업", process_sub_category="엘리베이터 가이드레일 설치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="엘리베이터 설치작업", process_sub_category="엘리베이터 승강구 조립"),
        ProcessCategory(process_main_category="공통공사", process_major_category="엘리베이터 설치작업", process_sub_category="엘리베이터 기계설치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="전기 설비작업", process_sub_category="전기설비 설치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="전기 설비작업", process_sub_category="전기설비 배선"),
        ProcessCategory(process_main_category="공통공사", process_major_category="전기 설비작업", process_sub_category="전기설비 자재 반입, 가공, 운반"),
        ProcessCategory(process_main_category="공통공사", process_major_category="전기 설비작업", process_sub_category="전기 특고압 선로, 활선 및 전주시공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="제작장 설치 작업", process_sub_category="제작장 설치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="제작장 설치 작업", process_sub_category="제작장 부지 조성"),
        ProcessCategory(process_main_category="공통공사", process_major_category="조경작업", process_sub_category="조경부지정리"),
        ProcessCategory(process_main_category="공통공사", process_major_category="조경작업", process_sub_category="조경시공 및 설치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="조적, 미장 및 견출작업", process_sub_category="조적 시공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="조적, 미장 및 견출작업", process_sub_category="미장 및 견출시공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="조적, 미장 및 견출작업", process_sub_category="자재반입 및 운반"),
        ProcessCategory(process_main_category="공통공사", process_major_category="지장물 조사 및 이설 작업", process_sub_category="지장물 되메움"),
        ProcessCategory(process_main_category="공통공사", process_major_category="지장물 조사 및 이설 작업", process_sub_category="지장물 조사 굴착"),
        ProcessCategory(process_main_category="공통공사", process_major_category="지장물 조사 및 이설 작업", process_sub_category="지장물 보호, 보강"),
        ProcessCategory(process_main_category="공통공사", process_major_category="지장물 조사 및 이설 작업", process_sub_category="지장물 이설"),
        ProcessCategory(process_main_category="공통공사", process_major_category="창호 및 유리작업", process_sub_category="자재반입, 가공, 운반"),
        ProcessCategory(process_main_category="공통공사", process_major_category="창호 및 유리작업", process_sub_category="창호 및 유리 설치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="철골 작업", process_sub_category="철골 부재 인양, 조립"),
        ProcessCategory(process_main_category="공통공사", process_major_category="철골 작업", process_sub_category="철골 부재반입 및 운반"),
        ProcessCategory(process_main_category="공통공사", process_major_category="철골 작업", process_sub_category="철골 데크플레이트 설치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="철근 작업", process_sub_category="철근 조립"),
        ProcessCategory(process_main_category="공통공사", process_major_category="철근 작업", process_sub_category="철근 가공 및 운반"),
        ProcessCategory(process_main_category="공통공사", process_major_category="철근 작업", process_sub_category="철근 반입"),
        ProcessCategory(process_main_category="공통공사", process_major_category="케이슨작업", process_sub_category="케이슨 제작"),
        ProcessCategory(process_main_category="공통공사", process_major_category="케이슨작업", process_sub_category="케이슨 운반 및 거치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="케이슨작업", process_sub_category="케이슨 내 속채움"),
        ProcessCategory(process_main_category="공통공사", process_major_category="콘크리트작업", process_sub_category="콘크리트 양생"),
        ProcessCategory(process_main_category="공통공사", process_major_category="콘크리트작업", process_sub_category="콘크리트 반입 운반"),
        ProcessCategory(process_main_category="공통공사", process_major_category="콘크리트작업", process_sub_category="콘크리트 타설 및 다짐"),
        ProcessCategory(process_main_category="공통공사", process_major_category="판넬등 외부 마감 작업", process_sub_category="판넬등 외부마감 시공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="판넬등 외부 마감 작업", process_sub_category="판넬 등 외부 마감 자재 반입"),
        ProcessCategory(process_main_category="공통공사", process_major_category="포설 및 다짐 작업", process_sub_category="포설 및 다짐"),
        ProcessCategory(process_main_category="공통공사", process_major_category="포장작업", process_sub_category="포장 시공"),
        ProcessCategory(process_main_category="공통공사", process_major_category="포장작업", process_sub_category="포장 장비 반입"),
        ProcessCategory(process_main_category="공통공사", process_major_category="흙막이 지보공 작업", process_sub_category="흙막이 지보공 해체"),
        ProcessCategory(process_main_category="공통공사", process_major_category="흙막이 지보공 작업", process_sub_category="자재반입"),
        ProcessCategory(process_main_category="공통공사", process_major_category="흙막이 지보공 작업", process_sub_category="흙막이 지보공 설치"),
        ProcessCategory(process_main_category="공통공사", process_major_category="흙막이 지보공 작업", process_sub_category="자재반출"),
        ProcessCategory(process_main_category="교량공사", process_major_category="PSC 교량 작업", process_sub_category="슬라브 시공"),
        ProcessCategory(process_main_category="교량공사", process_major_category="PSC 교량 작업", process_sub_category="거더 인양 및 거치"),
        ProcessCategory(process_main_category="교량공사", process_major_category="PSC 교량 작업", process_sub_category="Cross Beam 설치"),
        ProcessCategory(process_main_category="교량공사", process_major_category="PSC 교량 작업", process_sub_category="PSC 거더 제작"),
        ProcessCategory(process_main_category="교량공사", process_major_category="PSC 교량 작업", process_sub_category="거더 인양 및 상차"),
        ProcessCategory(process_main_category="교량공사", process_major_category="PSC 교량 작업", process_sub_category="거더 운반"),
        ProcessCategory(process_main_category="교량공사", process_major_category="강교 설치 작업", process_sub_category="강교 부재반입"),
        ProcessCategory(process_main_category="교량공사", process_major_category="강교 설치 작업", process_sub_category="강교 부재 운반, 인양"),
        ProcessCategory(process_main_category="교량공사", process_major_category="강교 설치 작업", process_sub_category="강교 조립"),
        ProcessCategory(process_main_category="교량공사", process_major_category="강교 설치 작업", process_sub_category="강교 슬라브 시공 "),
        ProcessCategory(process_main_category="교량공사", process_major_category="교량 가설작업", process_sub_category="MSS공법"),
        ProcessCategory(process_main_category="교량공사", process_major_category="교량 가설작업", process_sub_category="FCM공법"),
        ProcessCategory(process_main_category="교량공사", process_major_category="교량 가설작업", process_sub_category="사장교"),
        ProcessCategory(process_main_category="교량공사", process_major_category="교량 가설작업", process_sub_category="현수교"),
        ProcessCategory(process_main_category="교량공사", process_major_category="교량 가설작업", process_sub_category="ILM공법"),
        ProcessCategory(process_main_category="터널공사", process_major_category="갱구부 작업", process_sub_category="벌목 및 표토제거"),
        ProcessCategory(process_main_category="터널공사", process_major_category="갱구부 작업", process_sub_category="갱구부 보강"),
        ProcessCategory(process_main_category="터널공사", process_major_category="거푸집작업", process_sub_category="라이닝 거푸집 자재 반입, 하역"),
        ProcessCategory(process_main_category="터널공사", process_major_category="거푸집작업", process_sub_category="라이닝 거푸집 해체"),
        ProcessCategory(process_main_category="터널공사", process_major_category="거푸집작업", process_sub_category="라이닝 거푸집 설치"),
        ProcessCategory(process_main_category="터널공사", process_major_category="배수작업", process_sub_category="터널 배수 작업"),
        ProcessCategory(process_main_category="터널공사", process_major_category="굴착작업", process_sub_category="터널 굴착 장약"),
        ProcessCategory(process_main_category="터널공사", process_major_category="굴착작업", process_sub_category="터널 천공"),
        ProcessCategory(process_main_category="터널공사", process_major_category="굴착작업", process_sub_category="터널 버럭처리"),
        ProcessCategory(process_main_category="터널공사", process_major_category="굴착작업", process_sub_category="터널 발파"),
        ProcessCategory(process_main_category="터널공사", process_major_category="방수작업", process_sub_category="터널방수 작업"),
        ProcessCategory(process_main_category="터널공사", process_major_category="터널보강 작업", process_sub_category="특수보강"),
        ProcessCategory(process_main_category="터널공사", process_major_category="터널보강 작업", process_sub_category="락볼트"),
        ProcessCategory(process_main_category="터널공사", process_major_category="터널보강 작업", process_sub_category="강지보"),
        ProcessCategory(process_main_category="터널공사", process_major_category="터널보강 작업", process_sub_category="숏크리트"),
        ProcessCategory(process_main_category="터널공사", process_major_category="굴착작업", process_sub_category="특수터널(TBM)공법"),
        ProcessCategory(process_main_category="터널공사", process_major_category="굴착작업", process_sub_category="특수터널(SHIELD) 공법"),
    ],
    equipment_list=[
        Equipment(equipment="PSC빔"),
        Equipment(equipment="SHIELD머신"),
        Equipment(equipment="TBM머신"),
        Equipment(equipment="가설기자재"),
        Equipment(equipment="강관동바리"),
        Equipment(equipment="개구부"),
        Equipment(equipment="개인보호구"),
        Equipment(equipment="갱폼"),
        Equipment(equipment="거푸집"),
        Equipment(equipment="경사면"),
        Equipment(equipment="고소작업대"),
        Equipment(equipment="고소작업차"),
        Equipment(equipment="곤도라"),
        Equipment(equipment="공구류"),
        Equipment(equipment="굴삭기"),
        Equipment(equipment="굴착기"),
        Equipment(equipment="굴착사면"),
        Equipment(equipment="그라우팅 혼합기"),
        Equipment(equipment="그라우팅장비"),
        Equipment(equipment="기성말뚝"),
        Equipment(equipment="기중기(이동식 크레인 등)"),
        Equipment(equipment="기타 가시설"),
        Equipment(equipment="낙하물방지망"),
        Equipment(equipment="달비계"),
        Equipment(equipment="덤프트럭"),
        Equipment(equipment="데크플레이트"),
        Equipment(equipment="롤러"),
        Equipment(equipment="리어카"),
        Equipment(equipment="리프트"),
        Equipment(equipment="말비계"),
        Equipment(equipment="바지선"),
        Equipment(equipment="발파기"),
        Equipment(equipment="발파매트"),
        Equipment(equipment="방호선반"),
        Equipment(equipment="배관"),
        Equipment(equipment="불도저"),
        Equipment(equipment="비계"),
        Equipment(equipment="비산물"),
        Equipment(equipment="사다리"),
        Equipment(equipment="세그먼트"),
        Equipment(equipment="슬래브"),
        Equipment(equipment="승강기"),
        Equipment(equipment="아스팔트피니셔"),
        Equipment(equipment="안전시설물"),
        Equipment(equipment="암사면"),
        Equipment(equipment="양수기"),
        Equipment(equipment="에어콤프레셔"),
        Equipment(equipment="열풍기"),
        Equipment(equipment="예인선"),
        Equipment(equipment="옹벽"),
        Equipment(equipment="와이어로프"),
        Equipment(equipment="용접기"),
        Equipment(equipment="운반차량"),
        Equipment(equipment="이동식비계"),
        Equipment(equipment="인양장비"),
        Equipment(equipment="작업대차"),
        Equipment(equipment="작업발판"),
        Equipment(equipment="전기뇌관"),
        Equipment(equipment="전기설비"),
        Equipment(equipment="전도방지재"),
        Equipment(equipment="전동공구"),
        Equipment(equipment="전선"),
        Equipment(equipment="전주"),
        Equipment(equipment="조명"),
        Equipment(equipment="지게차"),
        Equipment(equipment="지지대"),
        Equipment(equipment="차량"),
        Equipment(equipment="천공기"),
        Equipment(equipment="철골부재"),
        Equipment(equipment="철근 가공기"),
        Equipment(equipment="철근부재"),
        Equipment(equipment="체인블록"),
        Equipment(equipment="추락방지망"),
        Equipment(equipment="캔틸레버"),
        Equipment(equipment="케이슨"),
        Equipment(equipment="콘크리트 진동기"),
        Equipment(equipment="콘크리트 피니셔"),
        Equipment(equipment="콘크리트믹서트럭"),
        Equipment(equipment="콘크리트살포기"),
        Equipment(equipment="콘크리트펌프"),
        Equipment(equipment="크람셀"),
        Equipment(equipment="크레인"),
        Equipment(equipment="크레인, 굴삭기"),
        Equipment(equipment="타워크레인"),
        Equipment(equipment="특수거푸집"),
        Equipment(equipment="특수건설기계"),
        Equipment(equipment="파일커터장비"),
        Equipment(equipment="항타기"),
        Equipment(equipment="해상크레인"),
        Equipment(equipment="핸드그라인더"),
        Equipment(equipment="혼합기"),
        Equipment(equipment="흙막이가시설"),
    ],
    material_list=[
        Material(material="가스"),
        Material(material="갈탄"),
        Material(material="그라우팅 약액"),
        Material(material="나무"),
        Material(material="낙석"),
        Material(material="낙하물"),
        Material(material="방수쉬트"),
        Material(material="벽돌"),
        Material(material="볼트"),
        Material(material="부석"),
        Material(material="분진"),
        Material(material="비산"),
        Material(material="비산물"),
        Material(material="사석"),
        Material(material="숏크리트"),
        Material(material="아스팔트"),
        Material(material="약액(규산소다)"),
        Material(material="유독가스"),
        Material(material="인화물질"),
        Material(material="자재"),
        Material(material="전류"),
        Material(material="철근"),
        Material(material="콘크리트"),
        Material(material="파편"),
        Material(material="페인트"),
        Material(material="화약"),
        Material(material="화약류"),
    ]
)



class ModelListRouter(BaseRouter):
    def __init__(self):
        super().__init__(prefix="/v1/list", tags=["List of Models"])

    def _register_routes(self):
        ##### 모델 목록 조회 관련 라우트 등록 #####
        self.router.add_api_route(
            path="/models",
            endpoint=self.get_all_models,
            methods=["GET"],
            response_model=Providers,
            description=self.get_all_models.__doc__
        )
        self.router.add_api_route(
            path="/models/output_schema",
            endpoint=self.get_output_schema(Providers),
            methods=["GET"],
            description="`/v1/list/models`의 OUTPUT 스키마를 조회합니다."
        )

        ##### 특정 제공자의 모델 목록 조회 관련 라우트 등록 #####
        self.router.add_api_route(
            path="/models/{provider}",
            endpoint=self.get_models,
            methods=["GET"],
            response_model=Provider,
            description="특정 제공자의 모델 목록을 조회하거나, 사용 가능한 모델만 필터링합니다."
        )
        self.router.add_api_route(
            path="/models/{provider}/input_schema",
            endpoint=self.get_input_schema(Provider),
            methods=["GET"],
            description="`/v1/list/models`의 INPUT 스키마를 조회합니다."
        )
        self.router.add_api_route(
            path="/models/{provider}/output_schema",
            endpoint=self.get_output_schema(Provider),
            methods=["GET"],
            description="`/v1/list/models`의 OUTPUT 스키마를 조회합니다."
        )

        ##### 입력 시트 목록 조회 관련 라우트 등록 #####
        self.router.add_api_route(
            path="/inputs",
            endpoint=self.get_all_inputs,
            methods=["GET"],
            response_model=InputSheets,
            description="모든 입력 시트 목록을 조회합니다."
        )
        self.router.add_api_route(
            path="/inputs/{input_label}",
            endpoint=self.get_inputs,
            methods=["GET"],
            response_model=List[ProcessCategory] | List[Equipment] | List[Material],
            description="특정 입력 레이블에 대한 입력 시트 목록을 조회합니다."
        )

    def get_all_models(
            self,
            filter: Literal["all", "available"] = Query("available", description="Filter type: 'all' or 'available'"),
        ) -> List[Provider]:
        """
        모든 언어 모델 목록을 조회하거나, 사용 가능한 모델만 필터링합니다.
        """
        if filter == "all":
            return language_models
        elif filter == "available":
            return Providers(
                items=[
                    Provider(
                        name=lm.name,
                        alias=lm.alias,
                        models=[model for model in lm.models if model.available]
                    ) for lm in language_models.items
                ]
            )
        else:
            raise HTTPException(400, detail="Invalid filter type. Use 'all' or 'available'.")

    def get_models(
            self,
            provider: EnumProviderAlias,
            filter: Literal["all", "available"] = Query("available", description="Filter type: 'all' or 'available'"),
        ) -> Provider:
        lm = next((lm for lm in language_models.items if lm.name.lower() == provider.lower() or lm.alias.lower() == provider.lower()), None)
        if not lm:
            raise HTTPException(404, f"Provider '{provider}' not found.")
        if filter == "all":
            return lm
        elif filter == "available":
            return Provider(
                name=lm.name,
                alias=lm.alias,
                models=[model for model in lm.models if model.available]
            )
        else:
            raise HTTPException(400, detail="Invalid filter type. Use 'all' or 'available'.")
        
    def get_all_inputs(self) -> InputSheets:
        return input_sheets
    
    @staticmethod
    def _get_main_category(
        handler: List[ProcessCategory], 
        main: Optional[Literal["공통공사", "교량공사", "터널공사"]]
    ) -> List[ProcessCategory]:
        if not main:
            return handler
        return [proc for proc in handler if proc.process_main_category == main]
    
    @staticmethod
    def _get_major_category(
        handler: List[ProcessCategory],
        major: Optional[str]
    ) -> List[ProcessCategory]:
        if not major:
            return handler
        return [proc for proc in handler if proc.process_major_category == major]
    
    def get_inputs(self, 
        input_label: Literal["process", "equipment", "material"],
        main: Literal["공통공사", "교량공사", "터널공사", ""] = Query(
            "", 
            description="작업 공정 대분류",
            examples=["공통공사", "교량공사", "터널공사"]
        ),
        major: str = Query(
            "", 
            description="작업 공정 중분류",
            examples=["거푸집작업", "가설 작업", "굴착작업"]
        ) 
    ) -> List[ProcessCategory] | List[Equipment] | List[Material]:
        if input_label == "process":
            output_handler = input_sheets.process_mapping
            output_handler = self._get_main_category(output_handler, main)
            output_handler = self._get_major_category(output_handler, major)
            return output_handler
        elif input_label == "equipment":
            return input_sheets.equipment_list
        elif input_label == "material":
            return input_sheets.material_list
        else:
            raise HTTPException(404, detail=f"Input label '{input_label}' not found.")
    

__all__ = ["ModelListRouter"]

