from typing import List

from fastapi import APIRouter
from langserve import add_routes


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
                input_type=chain.get("input_type")
            )
