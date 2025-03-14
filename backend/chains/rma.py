import os
from typing import List, Dict, Union
from langchain_core.documents import Document
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
from utils import print_return

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

@print_return
def encode_image_url(file_path: str) -> str:
    import base64
    with open(file_path, "rb") as file:
        base64_image = base64.b64encode(file.read()).decode('utf-8')
    file_ext = file_path.split(".")[-1]
    return f"data:image/{file_ext};base64, {base64_image}"

@print_return
def image_preprocessor(image_paths: Union[str, List[str]]) -> List[str]:
    if isinstance(image_paths, str):
        image_paths = [image_paths]
    
    processed_images = []
    for image_path in image_paths:
        _condition = "http://" in image_path or "https://" in image_path
        processed_images.append(image_path if _condition else encode_image_url(image_path))
    
    return processed_images

with open("prompts.yaml", "r", encoding="utf-8") as f:
    raw = yaml.safe_load(f)
    
raw_prompt = raw["rma"]

prompt = ChatPromptTemplate([
    ("system", raw_prompt["system"]),
    ("user", "{image_paths}"),  
    ("user", raw_prompt["user"].format(
            work_type="{work_type}", 
            procedure="{procedure}", 
            count="{count}",
        reference="{reference}", 
        related_law="{related_law}"
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
rma_chain = (
    RunnableParallel(
        {
            "image_paths": lambda x: image_preprocessor(x.get("image_paths", [])),
            "count": lambda x: x["count"],
            "work_type": lambda x: x["work_type"],
            "procedure": lambda x: x["procedure"],
            "reference": dict2str | RunnablePassthrough() | ref_retriever | format_docs,
            "related_law": dict2str | RunnablePassthrough() | legal_retriever | format_docs,
        }
    ) 
    | printer
    | prompt
    | printer
    | structured_output
    | printer
)

__all__ = ["rma_chain"]

if __name__ == "__main__":
    from utils import pretty_print_risk_evaluation

    result = rma_chain.invoke(
        {
            "image_paths": [
                "https://i.ytimg.com/vi/qZAB_yWWbU8/maxresdefault.jpg", 
                "https://lh5.googleusercontent.com/proxy/3Bn2dIDlQPZVwEmlBAPO4zafsqgJqm3kmwgBogbS9rMxjJrmHjODRLifzbxHnHkvRK9DLFN0XPnJvT8CiMvRoQ"
            ], 
            "count": "10", 
            "work_type": "철근 작업", 
            "procedure": "자재 운반"
        }
    )
    pretty_print_risk_evaluation(result.공종, result.공정, result.작업명, result.위험성평가표, result.기타)
