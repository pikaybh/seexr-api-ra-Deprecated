from langserve import add_routes

from chains import configure_chains

from models import BaseRouter
from utils import model_call


gpt_4o_chains = configure_chains(incorporation="openai", model="gpt-4o", embeddings="text-embedding-ada-002")
gpt_4o_mini_chains = configure_chains(incorporation="openai", model="gpt-4o-mini", embeddings="text-embedding-ada-002")

class OpenAIRouterV1(BaseRouter):
    def __init__(self):
        super().__init__(prefix="/v1/openai", tags=["OpenAI"])

    def _register_routes(self):
        add_routes(self.router, model_call(address="openai/gpt-4o"), path="/gpt-4o")
        
        ####### Add Chain Routes #######
        self.add_chain_routes(gpt_4o_chains)
        self.add_chain_routes(gpt_4o_mini_chains)


__all__ = ["OpenAIRouterV1"]
