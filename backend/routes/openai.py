from langchain_ollama import ChatOllama
from langserve import add_routes

from chains import configure_chains

from models import BaseRouter
from utils import model_call


OLLAMA_URL = "ollama.seexr.co.kr"

gpt_41_chains = configure_chains(incorporation="openai", model="gpt-4.1", embeddings="text-embedding-3-large")  # "text-embedding-ada-002")
gpt_4o_chains = configure_chains(incorporation="openai", model="gpt-4o", embeddings="text-embedding-3-large")  # "text-embedding-ada-002")
gpt_4o_mini_chains = configure_chains(incorporation="openai", model="gpt-4o-mini", embeddings="text-embedding-3-large")  # text-embedding-ada-002")
gpt_oss_120b_chains = configure_chains(incorporation="openai", model="gpt-oss:120b", embeddings="text-embedding-3-large", isollama=True)

class OpenAIRouterV1(BaseRouter):
    def __init__(self):
        super().__init__(prefix="/v1/openai", tags=["OpenAI"])

    def _register_routes(self):
        add_routes(self.router, model_call(address="openai/gpt-4.1"), path="/gpt-4.1")
        add_routes(self.router, model_call(address="openai/gpt-4o"), path="/gpt-4o")
        add_routes(self.router, ChatOllama(model="gpt-oss:120b", base_url=OLLAMA_URL), path="/oss-120b")
        
        ####### Add Chain Routes #######
        self.add_chain_routes(gpt_41_chains)
        self.add_chain_routes(gpt_4o_chains)
        self.add_chain_routes(gpt_4o_mini_chains)
        self.add_chain_routes(gpt_oss_120b_chains)


__all__ = ["OpenAIRouterV1"]
