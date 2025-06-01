from pydantic import BaseModel, Field
from typing import List, Literal


EnumProviderName = Literal["OpenAI", "DeepSeek", "LG AI"]
EnumProviderAlias = Literal[
    "OpenAI", "openai", 
    "DeepSeek", "ds", 
    "LG AI", "lgai"
]

class LargeLanguageModel(BaseModel):
    """
    Represents a large language model (LLM) with its configuration.
    """
    name: str = Field(description="LLM의 이름.")
    type: Literal["chat", "embedding", "completion"] = Field(
        description="LLM의 유형: 'chat', 'embedding', 또는 'completion'."
    )
    available: bool = Field(
        default=True, 
        description="본 LLM이 사용 가능하게 구현 되어 있는지 여부."
    )

class Provider(BaseModel):
    """
    대형 언어 모델(LLM) 제공 업체를 나타냅니다.
    """
    name: EnumProviderName = Field(
        description="LLM 제공 업체 상호명.",
        examples=["OpenAI", "DeepSeek"]
    )
    alias: EnumProviderAlias = Field(description="제공자의 별칭(옵션).")
    models: List[LargeLanguageModel] = Field(description="본 제공 업체가 제공하는 LLM 목록.")

class Providers(BaseModel):
    """
    LLM 제공 업체 목록을 나타냅니다.
    """
    items: List[Provider] = Field(description="LLM 제공 업체 목록.")

__all__ = [
    "LargeLanguageModel",
    "Provider",
    "EnumProviderName",
    "EnumProviderAlias",
    "Providers",
]