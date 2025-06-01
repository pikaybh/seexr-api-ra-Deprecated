from typing import Callable, List

from fastapi import APIRouter
from langserve import add_routes
from pydantic import BaseModel


__all__ = ["BaseRouter"]



class BaseRouter:
    def __init__(self, prefix: str, tags: List[str]):
        self.router = APIRouter(prefix=prefix, tags=tags)

    def configure(self) -> APIRouter:
        self._register_routes()
        return self.router

    def _register_routes(self):
        raise NotImplementedError
    
    def add_chain_routes(self, chains: List[dict]):
        for chain in chains:
            add_routes(
                self.router, 
                chain["chain"], 
                path=chain["path"], 
                input_type=chain.get("input_type", "auto"),
                output_type=chain.get("output_type", "auto")
            )

    def get_input_schema(self, schema: BaseModel) -> Callable:
        def input_schema():
            return schema.model_json_schema()
        input_schema.__name__ = f"{schema.__name__}InputSchema"
        input_schema.__doc__ = f"Input schema for {schema.__name__}"
        return input_schema
    
    def get_output_schema(self, schema: BaseModel) -> Callable:
        def output_schema():
            return schema.model_json_schema()
        output_schema.__name__ = f"{schema.__name__}OutputSchema"
        output_schema.__doc__ = f"Output schema for {schema.__name__}"
        return output_schema
        