from fastapi import APIRouter
from langserve import add_routes
from langchain_ollama import ChatOllama

from chains import (ra_chain, 
                    rma_chain,
                    RMAv2,
                    RMAv3,
                    rma_chain_text,
                    sample_item,
                    dummy_item,
                    RMAv2CY,
                    RMAv2BY,
                    CheckListV1)
from schemas import (KrasRiskAssessmentInput, 
                        KrasRiskMatrixAnalysisInput,
                        KrasRiskMatrixAnalysisInputText,
                        RiskAssessmentInput, RiskAssessmentOutput)
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
    RMAv2CY().chain_call(
        model="openai/gpt-4o", 
        embeddings="openai/text-embedding-ada-002"
    ),
    path="/openai/gpt-4o/test",
    input_type=RiskAssessmentInput
)
add_routes(
    v1_router,
    RMAv2CY().chain_call(
        model="openai/gpt-4o", 
        embeddings="openai/text-embedding-ada-002"
    ),
    path="/openai/gpt-4o/test_by",
    input_type=RiskAssessmentInput
)

## Checklist
add_routes(
    v1_router,
    CheckListV1().chain_call(
        model="openai/gpt-4o", 
        embeddings="openai/text-embedding-ada-002"
    ),
    path="/openai/gpt-4o/checklist",
    input_type=RiskAssessmentOutput
)

# Distributed
add_routes(
    v1_router, 
    RMAv2BY().chain_call(
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

@v1_router.post("/rma/test/")
async def rma_test():
    return dummy_item


__all__ = ["v1_router"]
