from fastapi import APIRouter
from fastapi_versioning import versioning
from langserve import add_routes
from langchain_ollama import ChatOllama

from chains import (ra_chain, 
                    rma_chain,
                    RMAv2,
                    RMAv3,
                    rma_chain_text,
                    sample_item)
from structures import (KrasRiskAssessmentInput, 
                        KrasRiskMatrixAnalysisInput,
                        KrasRiskMatrixAnalysisInputText)
from utils import model_call  # , quantized_model_call


OLLAMA_URL = "http://snucem1.iptime.org:11434"

v1_router = APIRouter(prefix="/v1", tags=["v1"])

# OpenAI
openai_gpt_4o = model_call(address="openai/gpt-4o")

# Ollama
# ollama_deepseek_r1 = quantized_model_call(address="ollama/deepseek-r1:32b")
# ollama_exaone_35 = quantized_model_call(address="ollama/exaone3.5:latest")
ollama_deepseek_r1 = ChatOllama(model="deepseek-r1:32b", base_url=OLLAMA_URL)
ollama_exaone_35 = ChatOllama(model="exaone3.5:latest", base_url=OLLAMA_URL)

add_routes(v1_router, openai_gpt_4o, path="/openai/gpt-4o")
add_routes(v1_router, ollama_deepseek_r1, path="/ollama/ds-r1")
add_routes(v1_router, ollama_exaone_35, path="/ollama/exaone-35")

add_routes(v1_router, ra_chain, path="/ra", input_type=KrasRiskAssessmentInput)
add_routes(v1_router, rma_chain, path="/rma", input_type=KrasRiskMatrixAnalysisInput)
add_routes(
    v1_router, 
    RMAv2().chain_call(
        model="openai/gpt-4o", 
        embeddings="openai/text-embedding-ada-002"
    ), 
    path="/openai/gpt-4o/rmav2", 
    input_type=KrasRiskMatrixAnalysisInput
)
add_routes(
    v1_router, 
    RMAv3().chain_call(
        model="openai/gpt-4o", 
        embeddings="openai/text-embedding-ada-002"
    ), 
    path="/openai/gpt-4o/rmav3", 
    input_type=KrasRiskMatrixAnalysisInput
)
add_routes(
    v1_router, 
    RMAv2().chain_call(
        model="exaone3.5:latest", 
        embeddings="openai/text-embedding-ada-002"
    ), 
    path="/ollama/exaone-35/rmav2", 
    input_type=KrasRiskMatrixAnalysisInput
)
add_routes(v1_router, rma_chain_text, path="/rma-text", input_type=KrasRiskMatrixAnalysisInputText)


'''
@v1_router.post("/ra")
def ra(input: KrasRiskAssessmentInput, x_api_key: str = Header(...)) -> KrasRiskAssessmentOutput:
    if not verify_access_token(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return ra_chain(input)

@v1_router.post("/ra/{userid}")
def ra(input: KrasRiskAssessmentInput, session: str = Header(...)) -> KrasRiskAssessmentOutput:
    """TODO: Implement this"""
    if not 1:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return ra_chain(input)
'''

@v1_router.post("/ra/test")
async def ra_test():
    return sample_item


__all__ = ["v1_router"]
