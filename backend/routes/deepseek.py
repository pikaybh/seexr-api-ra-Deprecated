from langchain_ollama import ChatOllama
from langserve import add_routes

# from chains import configure_chains

from models import BaseRouter


OLLAMA_URL = "http://snucem1.iptime.org:11434"

deepseek_r1 = ChatOllama(model="deepseek-r1:32b", base_url=OLLAMA_URL)
# deepseek_r1_chains = configure_chains(incorporation="ollama", 
#                                      model="deepseek-r1:32b", 
#                                      embeddings="text-embedding-ada-002")

class DeepSeekRouterV1(BaseRouter):
    def __init__(self):
        super().__init__(prefix="/v1/ds", tags=["DeepSeek"])

    def _register_routes(self):
        add_routes(self.router, deepseek_r1, path="/r1")
        
        ####### Add Chain Routes #######
        # self.add_chain_routes(deepseek_r1_chains)


__all__ = ["DeepSeekRouterV1"]
