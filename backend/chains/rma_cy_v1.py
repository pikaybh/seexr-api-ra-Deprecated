import os
from typing import List, Dict
from langchain_core.documents import Document
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.vectorstores import FAISS, Chroma
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
import yaml

from dotenv import load_dotenv

from structures import KrasRiskAssessmentOutput, kras_map

load_dotenv()

model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=os.getenv("OPENAI_API_KEY"))

# KRAS
ref_path = "assets/faiss/faiss_K+S+O_Openai"
ref_vectorstores = FAISS.load_local(ref_path, embeddings, allow_dangerous_deserialization=True)
ref_retriever = ref_vectorstores.as_retriever(search_type="similarity", search_kwargs={"k": 20})
import functools

def print_return(func):
    """함수의 반환 값을 출력하는 데코레이터"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)  # 함수 실행
        print(f"🔹 {func.__name__}: {result}")  # 결과 출력
        return result  # 원래 반환 값 유지
    return wrapper

with open("prompts.yaml", "r", encoding="utf-8") as f:
    raw = yaml.safe_load(f)
    
raw_prompt = raw["cy_rma_v2"]

prompt = ChatPromptTemplate([
    ("system", raw_prompt["system"]),
    ("user", raw_prompt["user"].format(
        work_type="{work_type}", 
        procedure="{procedure}", 
        count="{count}",
        reference="{reference}"
    ))
])

# Select Data
def select_data(key: str) -> str:
    def _select_data(data):
        return data[key]
    return _select_data

def mapper(map: Dict[str, str], *args) -> str:
    valid_items = [f"{key}: {value}" for key, value in map.items() if value in args]
    return "\n".join(valid_items)

# Map Dictionary to String
def dict2str(data) -> str:
    if isinstance(data, str):
        return data  # 이미 str이면 그대로
    return mapper(kras_map, *data.keys())

# Formatter Configuration
def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)

@print_return
def printer(data):
    return data

# Output Configuration
structured_output = model.with_structured_output(KrasRiskAssessmentOutput)

# Chain Configuration
rma_chain_text = (
    RunnableParallel(
        {
            "count": lambda x: x["count"],
            "work_type": lambda x: x["work_type"],      # 공종
            "procedure": lambda x: x["procedure"],      # 공정
            "reference": dict2str | RunnablePassthrough() | ref_retriever | format_docs     # 유사 작업
        }
    ) 
    | printer
    | prompt
    | printer
    | structured_output
    | printer
)

__all__ = ["rma_chain_text"]

if __name__ == "__main__": 
    from utils import pretty_print_risk_evaluation
    import json
    
    result = rma_chain_text.invoke(
        {
            "count": "15", 
            "work_type": "금일 작업은 아파트 신축 현장 5층 슬래브 구간에서 동바리 설치를 진행한다. 콘크리트 타설 전 거푸집을 지지하기 위한 구조물로서, 설계 도면을 기준으로 동바리의 간격과 높이를 정확히 맞추어 설치하며, 수평·수직 상태를 확인한 후 레벨 조정 및 고정 작업을 수행한다. 설치 과정 중에는 구조물의 흔들림이나 처짐이 발생하지 않도록 추가 지지대를 보강하고, 설치 완료 후에는 팀 내 자체 점검을 실시한 뒤 안전관리자의 최종 점검을 받는다.", 
            "procedure": ""
        }
    )
    
    # 결과 데이터 구조 확인을 위한 로깅
    print("\n===== 결과 데이터 구조 =====")
    print(f"위험성평가표 타입: {type(result.위험성평가표)}")
    if hasattr(result, '위험성평가표') and result.위험성평가표:
        if isinstance(result.위험성평가표, list):
            print(f"위험성평가표 항목 수: {len(result.위험성평가표)}")
            if result.위험성평가표:
                print(f"첫 번째 항목 타입: {type(result.위험성평가표[0])}")
                print(f"첫 번째 항목 속성: {dir(result.위험성평가표[0])}")
    
    # 원래 함수 호출
    pretty_print_risk_evaluation(result.공종, result.공정, result.작업명, result.위험성평가표, result.기타)

