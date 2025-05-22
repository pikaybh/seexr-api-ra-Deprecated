from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class BaseResponse(BaseModel):
    """
    Base response model for all API responses.
    """
    status: str = Field(description="Response status")
    code: int = Field(description="Response code")
    message: str = Field(description="Response message")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Response data")
    error: Optional[str] = Field(default=None, description="Error message if any")

__all__ = [
    "BaseResponse",
]