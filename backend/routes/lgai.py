from langchain_ollama import ChatOllama
from langserve import add_routes

# from chains import configure_chains

from models import BaseRouter


OLLAMA_URL = "http://snucem1.iptime.org:11434"

exaone_35 = ChatOllama(model="exaone3.5:latest", base_url=OLLAMA_URL)
# exaone_35_chains = configure_chains(incorporation="ollama", 
#                                      model="exaone3.5:latest", 
#                                      embeddings="text-embedding-ada-002")

class LGAIRouterV1(BaseRouter):
    def __init__(self):
        super().__init__(prefix="/v1/lgai", tags=["LG AI"])

    def _register_routes(self):
        add_routes(self.router, exaone_35, path="/exaone-35")
        
        ####### Add Chain Routes #######
        # self.add_chain_routes(exaone_35_chains)


__all__ = ["LGAIRouterV1"]
