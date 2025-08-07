import base64, os, re
from typing import Any, Callable, Dict, List, Optional, Union

import yaml
from pydantic import BaseModel
from langchain_core.runnables import RunnableParallel
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS  # , Chroma
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever  # , InMemoryVectorStore
from langchain.prompts import BasePromptTemplate, PromptTemplate, ChatPromptTemplate, FewShotPromptTemplate, PipelinePromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.embeddings import Embeddings
from rich.console import Console
from rich.table import Table
from rich.box import ROUNDED

from utils import model_call, print_return  # , quantized_model_call


PROMPT_PATH: str = "prompts.yaml"
FAISS_PATH: str = "assets/faiss"
OLLAMA_URL = "http://snucem1.iptime.org:11434"



class ChainBase(BaseModel):
    _model: BaseLanguageModel
    _embeddings: Embeddings
    _prompt: Dict[str, str | list | dict]
    _chain: Dict[str, Any]

    @property
    def chain(self) -> Dict[str, Any]:
        return self._chain
    
    @chain.setter
    def chain(self, value: Dict[str, Any]):
        self._chain = value

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
            if "gpt-oss" in value:
                self._model = ChatOllama(model=value, base_url="ollama.seexr.co.kr")
            else:
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

    def parallel_init(self, *args, **kwargs) -> RunnableParallel:
        @print_return
        def _parallel_init(*args, **kwargs) -> RunnableParallel:
            return RunnableParallel(*args, **kwargs)
        return _parallel_init(*args, **kwargs)

    def faiss_retrieval(self, 
                        file_name: str, 
                        storage_kwargs: Optional[dict]={
                            "allow_dangerous_deserialization": True
                        }, 
                        retriever_kwargs: Optional[dict]={
                            "search_type": "similarity",  # similarity_score_threshold로 했을 때 의미가 없었음 (최소 `{'score_threshold': 0.4}` 이상).
                            "search_kwargs": {"k": 7}
                        }) -> Callable:
        path = os.path.join(FAISS_PATH, file_name)
        vectorstores: VectorStore = FAISS.load_local(path, self.embeddings, **storage_kwargs)
        retriever: VectorStoreRetriever = vectorstores.as_retriever(**retriever_kwargs)
        # @print_return
        # def retrieve(*args, **kwargs) -> Any:
        #     # print(f"Retrieving {args = }, {kwargs = }")
        #     return retriever.invoke(*args, **kwargs)
        # return retrieve
        return lambda *args, **kwargs: retriever.invoke(*args, **kwargs)
    
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

    def mapper(self, mapping: Dict[str, str], **kwargs) -> str:
        valid_items = [
            f"{key}: {kwargs[value]}" 
            for key, value in mapping.items() 
            if value in kwargs.keys() 
            and key != "이미지" 
            and kwargs[value]
        ]
        return " ".join(valid_items)

    # Map Dictionary to String
    def get_dict2str(self, mapping: Dict[str, str]) -> Callable:
        @print_return
        def dict2str(data) -> str:
            return self.mapper(mapping, **data)
        return dict2str

    # Formatter Configuration
    def format_docs(self, docs: List[Document]) -> str:
        return "\n\n".join(doc.page_content for doc in docs)
    
    def format_docs(self, docs: List[Document]) -> str:
        return "\n\n".join(
            "\n".join(f"{key}: {value}" for key, value in doc.metadata.items())
            for doc in docs
            )
    
    @print_return
    def format_table(self, docs: List[Document]) -> str:
        rows = []
        for doc in docs:
            # key와 key 사이를 value로 인식하여 정확히 분리 (value가 여러 줄이거나 비어 있어도 안전)
            pairs = re.findall(r'([^:\n]+):\s*((?:(?![^:\n]+:).)*)', doc.page_content, re.DOTALL)
            row = {k.strip().lstrip("\ufeff"): v.strip() for k, v in pairs}
            rows.append(row)
        # 원하는 열 순서 지정
        preferred_order = ["공정", "세부공정", "설비", "물질", "유해위험요인", "감소대책", "사고분류"]
        all_keys = [k for k in preferred_order if any(k in row for row in rows)]
        # 나머지 키는 알파벳순으로 뒤에 추가
        extra_keys = sorted({k for row in rows for k in row if k not in preferred_order})
        all_keys += [k for k in extra_keys if k not in all_keys]
        table = Table(show_header=True, 
                    header_style="bold magenta",
                    box=ROUNDED,
                    show_lines=True,
                    width=175)
        for key in all_keys:
            table.add_column(key, no_wrap=False, overflow="fold")
        for row in rows:
            table.add_row(*(row.get(k, "") for k in all_keys))
        console = Console(record=True)
        console.print(table, crop=False, overflow="fold")
        return console.export_text()

    @print_return
    def printer(self, data):
        return data
    
    def _register_chain(self, *args, **kwargs):
        raise NotImplementedError("`_register_chain` method not implemented.")
    
    def configure(self, **kwargs):
        self._register_chain(**kwargs)
        return self.chain



__all__ = ["ChainBase"]
