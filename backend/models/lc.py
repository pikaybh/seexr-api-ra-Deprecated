import base64
import os
from typing import Any, Callable, Dict, List, Optional, Union

import yaml
from pydantic import BaseModel
from langchain_core.runnables import RunnableParallel
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS, Chroma
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever, InMemoryVectorStore
from langchain.prompts import BasePromptTemplate, PromptTemplate, ChatPromptTemplate, FewShotPromptTemplate, PipelinePromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.embeddings import Embeddings

from utils import model_call, print_return  # , quantized_model_call


PROMPT_PATH: str = "prompts.yaml"
FAISS_PATH: str = "assets/faiss"
OLLAMA_URL = "http://snucem1.iptime.org:11434"



class ChainBase(BaseModel):
    _model: BaseLanguageModel
    _embeddings: Embeddings
    _prompt: Dict[str, str | list | dict]

    @property
    def model(self) -> BaseLanguageModel:
        return self._model
    
    @model.setter
    def model(self, value: str):
        """TODOs: `model_call` jmp point"""
        try:
            self._model = model_call(value)
        except:
            print(f"Model not found: {value}")
            from langchain_ollama import ChatOllama
            self._model = ChatOllama(model=value, base_url=OLLAMA_URL)
            # self._model = quantized_model_call(value)

    @property
    def embeddings(self) -> Embeddings:
        return self._embeddings
    
    @embeddings.setter
    def embeddings(self, value: str):
        self._embeddings = model_call(value)

    # Prompt
    @property
    def prompt(self) -> Dict[str, str | list | dict]:
        return self._prompt
    
    @prompt.setter
    def prompt(self, value: str):
        with open(PROMPT_PATH, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        self._prompt = raw[value]

    @print_return
    def parallel_init(self, *args, **kwargs) -> RunnableParallel:
        return RunnableParallel(*args, **kwargs)

    def faiss_retrieval(self, 
                        file_name: str, 
                        storage_kwargs: Optional[dict]={
                            "allow_dangerous_deserialization": True
                        }, 
                        retriever_kwargs: Optional[dict]={
                            "search_type": "similarity", 
                            "search_kwargs": {"k": 7}
                        }) -> Callable:
        path = os.path.join(FAISS_PATH, file_name)
        vectorstores: VectorStore = FAISS.load_local(path, self.embeddings, **storage_kwargs)
        retriever: VectorStoreRetriever = vectorstores.as_retriever(**retriever_kwargs)
        @print_return
        def retrieve(*args, **kwargs) -> Any:
            return retriever.invoke(*args, **kwargs)
        return retrieve
    
    def template_call(self, type: str = "chat", *args_template, **kwargs_template) -> BasePromptTemplate:
        if type == "prompt":
            @print_return
            def template(*args, **kwargs):
                return PromptTemplate(*args_template, **kwargs_template).invoke(*args, **kwargs)
        elif type == "chat":
            @print_return
            def template(*args, **kwargs):
                return ChatPromptTemplate(*args_template, **kwargs_template).invoke(*args, **kwargs)
        elif type == "few-shot":
            @print_return
            def template(*args, **kwargs):
                return FewShotPromptTemplate(*args_template, **kwargs_template).invoke(*args, **kwargs)
        elif type == "pipeline":
            @print_return
            def template(*args, **kwargs):
                return PipelinePromptTemplate(*args_template, **kwargs_template).invoke(*args, **kwargs)
        else:
            raise ValueError(f"`type` not supported: {type = }")
        return template

    @print_return
    def encode_image_url(self, file_path: str) -> str:
        with open(file_path, "rb") as file:
            base64_image = base64.b64encode(file.read()).decode('utf-8')
        file_ext = file_path.split(".")[-1]
        return f"data:image/{file_ext};base64, {base64_image}"

    @print_return
    def image_preprocessor(self, image_paths: Union[str, List[str]]) -> List[str]:
        if isinstance(image_paths, str):
            image_paths = [image_paths]
        
        processed_images = []
        for image_path in image_paths:
            _condition = "http://" in image_path or "https://" in image_path
            processed_images.append(image_path if _condition else self.encode_image_url(image_path))
        return processed_images

    # Select Data
    def select_data(self, key: str) -> str:
        def _select_data(data):
            return data[key]
        return _select_data

    def mapper(self, map: Dict[str, str], *args) -> str:
        valid_items = [f"{key}: {value}" for key, value in map.items() if value in args]
        return "\n".join(valid_items)

    # Map Dictionary to String
    def get_dict2str(self, mapping: Dict[str, str]) -> Callable:
        def dict2str(data) -> str:
            return self.mapper(mapping, *data.keys())
        return dict2str

    # Formatter Configuration
    def format_docs(self, docs: List[Document]) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    @print_return
    def printer(self, data):
        return data



__all__ = ["ChainBase"]
