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
ref_path = "assets/faiss/faiss_KRAS"
ref_vectorstores = FAISS.load_local(ref_path, embeddings, allow_dangerous_deserialization=True)
ref_retriever = ref_vectorstores.as_retriever(search_type="similarity", search_kwargs={"k": 7})

# Legal
legal_path = "assets/faiss/faiss_law_openai"
legal_vectorstores = FAISS.load_local(legal_path, embeddings, allow_dangerous_deserialization=True)
legal_retriever = legal_vectorstores.as_retriever(search_type="similarity", search_kwargs={"k": 7})

with open("prompts.yaml", "r", encoding="utf-8") as f:
    raw = yaml.safe_load(f)
    
raw_prompt = raw["ra"]

# Prompt Configuration   
# prompt = ChatPromptTemplate.from_messages(
#     messages=[
#         SystemMessage(content=raw_prompt["system"]),
#         HumanMessage(
#             content=raw_prompt["user"].format(
#                 work_type="{work_type}", 
#                 procedure="{procedure}", 
#                 reference="{reference}", 
#                 related_law="{related_law}"
#             )
#         )
#     ]
# )
prompt = ChatPromptTemplate([
    ("system", raw_prompt["system"]),
    ("user", raw_prompt["user"].format(
        work_type="{work_type}", 
        procedure="{procedure}", 
        reference="{reference}", 
        related_law="{related_law}")
    )
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
    return mapper(kras_map, *data.keys())

# Formatter Configuration
def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)

# Output Configuration
structured_output = model.with_structured_output(KrasRiskAssessmentOutput)

# Chain Configuration
ra_chain = (
    RunnableParallel(
        {
            "work_type": lambda x: x["work_type"],      # 공종
            "procedure": lambda x: x["procedure"],      # 공정
            "reference": dict2str | RunnablePassthrough() | ref_retriever | format_docs,     # 유사 작업
            "related_law": dict2str | RunnablePassthrough() | legal_retriever | format_docs,   # 근거 법령
        }
    ) 
    | prompt 
    | structured_output
)

__all__ = ["ra_chain"]

if __name__ == "__main__":
    print(ra_chain.invoke({"work_type": "철근 작업", "procedure": "자재 운반"}))