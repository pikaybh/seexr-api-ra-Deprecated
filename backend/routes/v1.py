from fastapi import APIRouter
from fastapi_versioning import versioning
from langserve import add_routes
from langchain_ollama import ChatOllama

from chains import (ra_chain, 
                    rma_chain,
                    RMA,
                    rma_chain_text,
                    sample_item)
from structures import (KrasRiskAssessmentInput, 
                        KrasRiskMatrixAnalysisInput,
                        KrasRiskMatrixAnalysisInputText,
                        KrasRiskAssessmentOutput)
from utils import model_call


v1_router = APIRouter(prefix="/v1", tags=["v1"])

# OpenAI
openai_gpt_4o = model_call(address="openai/gpt-4o")

# Ollama
model_deepseek_r1 = ChatOllama(model="deepseek-r1:32b")

# Resources
add_routes(v1_router, openai_gpt_4o, path="/openai")
add_routes(v1_router, model_deepseek_r1, path="/ds-r1")

add_routes(v1_router, ra_chain, path="/ra", input_type=KrasRiskAssessmentInput)
add_routes(v1_router, rma_chain, path="/rma", input_type=KrasRiskMatrixAnalysisInput)
add_routes(v1_router, RMA().chain_call(model="openai/gpt-4o", embeddings="openai/text-embedding-ada-002"), path="/rmav2", input_type=KrasRiskMatrixAnalysisInput)
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
async def ra_test(): return sample_item


__all__ = ["v1_router"]
