import os
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi_versioning import VersionedFastAPI, version
from langserve import add_routes
from langchain_openai import ChatOpenAI

from chains import (ra_chain, 
                    rma_chain,
                    rma_chain_text,
                    sample_item)
from structures import (KrasRiskAssessmentInput, 
                        KrasRiskMatrixAnalysisInput,
                        KrasRiskMatrixAnalysisInputText,
                        KrasRiskAssessmentOutput)

from langchain_ollama import ChatOllama

load_dotenv()

openai_router = APIRouter(prefix="/openai")

# Resources
add_routes(v1_router, openai_gpt_4o, path="/openai")
add_routes(v1_router, model_deepseek_r1, path="/ds-r1")

add_routes(v1_router, ra_chain, path="/ra", input_type=KrasRiskAssessmentInput)
add_routes(v1_router, rma_chain, path="/rma", input_type=KrasRiskMatrixAnalysisInput)
add_routes(v1_router, rma_chain_text, path="/rma-text", input_type=KrasRiskMatrixAnalysisInputText)


@v1_router.post("/ra/test")
async def ra_test(): return sample_item


__all__ = ["v1_router"]
