import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

from pydantic import BaseModel, computed_field
from langchain_core.language_models import BaseLanguageModel
from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_huggingface import ChatHuggingFace, HuggingFaceEmbeddings


load_dotenv()

MILLION: int = 1_000_000
# OLLAMA_BASE_URL = "http://localhost:11434"



class Pricing(BaseModel):
    input_per_1M_tokens: Optional[float] = None
    output_per_1M_tokens: Optional[float] = None

    @computed_field
    @property
    def input_price(self) -> float:
        return self.input_per_1M_tokens / MILLION
    
    @computed_field
    @property
    def output_price(self) -> float:
        return self.output_per_1M_tokens / MILLION



class LanguageModel(BaseModel):
    name: str
    pricing: Pricing
    is_embedding: Optional[bool] = False



class EncodingModel(BaseModel):
    name: str
    models: List[LanguageModel]



class Inc(BaseModel):
    name: str
    language_models: List[LanguageModel]
    encoding_models: List[EncodingModel]



# 이름 기반으로 모델을 찾을 수 있도록 딕셔너리 생성
def get_data_dict(datas: List[LanguageModel | EncodingModel | Inc]) -> Dict[str, LanguageModel | EncodingModel | Inc]:
    return {data.name: data for data in datas}


# 모델 이름을 `GPTModel` 객체로 변환하는 함수
def get_elements_by_names(data_names: List[str] | str, data: List[LanguageModel | EncodingModel | Inc]) -> List[LanguageModel | EncodingModel | Inc]:
    _data_dict = get_data_dict(data)
    
    if isinstance(data_names, str):
        return _data_dict[data_names]
    elif isinstance(data_names, list):
        return [_data_dict[name] for name in data_names if name in _data_dict]
    else:
        raise TypeError(f"{data_names} does not have valid type. ({type(data_names) = })")



class OpenAIPricing(Pricing):
    cached_input_per_1M_tokens: Optional[float] = None
    cost_per_1M_tokens: Optional[float] = None

    @computed_field
    @property
    def cached_input_price(self) -> float:
        # if not self.cached_input_per_1M_tokens:
        #     raise ValueError()
        return self.cached_input_per_1M_tokens / MILLION

    @computed_field
    @property
    def cost(self) -> float:
        # if not self.cost_per_1M_tokens:
        #     raise ValueError()
        return self.cost_per_1M_tokens / MILLION



class OpenAIModel(LanguageModel):
    pricing: OpenAIPricing



openai_language_models: List[OpenAIModel] = [
    OpenAIModel(name="gpt-o1", pricing=OpenAIPricing(input_per_1M_tokens=15.00, cached_input_per_1M_tokens=7.50, output_per_1M_tokens=60.00)),
    OpenAIModel(name="gpt-o3-mini", pricing=OpenAIPricing(input_per_1M_tokens=1.10, cached_input_per_1M_tokens=0.55, output_per_1M_tokens=4.40)),
    OpenAIModel(name="gpt-o1-mini", pricing=OpenAIPricing(input_per_1M_tokens=1.10, cached_input_per_1M_tokens=0.55, output_per_1M_tokens=4.40)),
    OpenAIModel(name="gpt-4.5", pricing=OpenAIPricing(input_per_1M_tokens=75.00, cached_input_per_1M_tokens=37.50, output_per_1M_tokens=150.00)),
    OpenAIModel(name="gpt-4o", pricing=OpenAIPricing(input_per_1M_tokens=2.50, cached_input_per_1M_tokens=1.25, output_per_1M_tokens=10.00)),
    OpenAIModel(name="gpt-4o-mini", pricing=OpenAIPricing(input_per_1M_tokens=0.150, cached_input_per_1M_tokens=0.075, output_per_1M_tokens=0.600)),
    OpenAIModel(name="gpt-4-turbo", pricing=OpenAIPricing(input_per_1M_tokens=10.00, output_per_1M_tokens=30.00)),
    OpenAIModel(name="gpt-4", pricing=OpenAIPricing(input_per_1M_tokens=30.00, output_per_1M_tokens=60.00)),
    OpenAIModel(name="gpt-3.5-turbo", pricing=OpenAIPricing(input_per_1M_tokens=0.50, output_per_1M_tokens=1.50)),
    OpenAIModel(name="text-embedding-3-small", pricing=OpenAIPricing(cost_per_1M_tokens=0.02), is_embedding=True),
    OpenAIModel(name="text-embedding-3-large", pricing=OpenAIPricing(cost_per_1M_tokens=0.13), is_embedding=True),
    OpenAIModel(name="text-embedding-ada-002", pricing=OpenAIPricing(cost_per_1M_tokens=0.10), is_embedding=True)
]

openai_encoding_models: List[EncodingModel] = [
    EncodingModel(name="o200k_base", models=get_elements_by_names(["gpt-4o", "gpt-4o-mini"], openai_language_models)),
    EncodingModel(name="cl100k_base", models=get_elements_by_names(["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo", "text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"], openai_language_models)),
    EncodingModel(name="p50k_base", models=get_elements_by_names(["text-davinci-002", "text-davinci-003"], openai_language_models)),
    EncodingModel(name="r50k_base", models=get_elements_by_names(["davinci"], openai_language_models)),
    EncodingModel(name="gpt2", models=get_elements_by_names(["davinci"], openai_language_models))
]

INCS: List[Inc] = [
    Inc(name="openai", language_models=openai_language_models, encoding_models=openai_encoding_models)
]



def model_call(address: str) -> BaseLanguageModel | Embeddings:
    """
    address `{inc.}/{model name}` 구조.
    """
    if not address.count('/') == 1:
        raise NameError()
    
    inc_name, model_name = address.split('/')
    models = get_elements_by_names(inc_name, INCS)
    model = get_elements_by_names(model_name, models.language_models)
    
    if inc_name == "openai":
        return OpenAIEmbeddings(model=model.name, api_key=os.getenv("OPENAI_API_KEY")) if model.is_embedding else \
            ChatOpenAI(model=model.name, api_key=os.getenv("OPENAI_API_KEY"))
    elif inc_name == "anthropic":
        return ChatAnthropic(model=model.name, api_key=os.getenv("ANTHROPIC_API_KEY"))
    else:
        return HuggingFaceEmbeddings(model=model.name) if model.is_embedding else ChatHuggingFace(model=model.name)


def quantized_model_call(address: str) -> BaseLanguageModel | Embeddings:
    """
    address `{inc.}/{model name}` 구조.
    """
    if not address.count('/') == 1:
        raise NameError()
    
    inc_name, model_name = address.split('/')
    models = get_elements_by_names(inc_name, INCS)
    model = get_elements_by_names(model_name, models)

    return OllamaEmbeddings(model.name) if model.is_embedding else ChatOllama(model.name)


__all__ = ["model_call", "quantized_model_call"]

if __name__ == "__main__":
    llm = model_call("openai/gpt-4o")
    result = llm.invoke("청주 날씨는 어때요?")
    print(result)