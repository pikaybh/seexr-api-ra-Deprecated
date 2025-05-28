from pydantic import BaseModel, Field
from typing import List, Literal


class LargeLanguageModel(BaseModel):
    """
    Represents a large language model (LLM) with its configuration.
    """
    name: str = Field(description="The name of the LLM.")
    type: Literal["chat", "embedding", "completion"] = Field(
        description="The type of LLM: 'chat', 'embedding', or 'completion'."
    )
    available: bool = Field(
        default=True, description="Indicates if the LLM is available for use."
    )

class Provider(BaseModel):
    """
    Represents a provider of large language models (LLMs).
    """
    name: str = Field(description="The name of the provider.")
    alias: str = Field(description="An optional alias for the provider.")
    models: List[LargeLanguageModel] = Field(description="List of LLMs provided by this provider.")

__all__ = [
    "LargeLanguageModel",
    "Provider",
]