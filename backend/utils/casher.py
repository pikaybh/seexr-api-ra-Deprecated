import tiktoken

from models import GPTModel, EncodingModel, encodings, gpt_model_dict


def get_model_instance(model: str) -> GPTModel | EncodingModel:
    """입력된 모델 이름이 GPT 모델인지, Encoding 모델인지 확인 후 반환"""
    if model in gpt_model_dict:
        return gpt_model_dict[model]
    
    for encoding in encodings:
        if model == encoding.name:
            return encoding

    raise ValueError(f"Unknown model or encoding: {model}")


def num_tokens_from_string(context: str, encoding_name: str) -> int:
    """주어진 문자열의 토큰 개수를 반환"""
    encoding = tiktoken.get_encoding(encoding_name) \
        if isinstance(get_model_instance(encoding_name), EncodingModel) \
        else tiktoken.encoding_for_model(encoding_name)
    return len(encoding.encode(context))


def calc_input(context: str, encoding_name: str) -> float:
    """
    주어진 문맥(context)에서 입력 토큰 개수 기반으로 비용 계산
    
    ```
        >> print(f"${calc_input(lorem, "gpt-4o"):,.2}")
        $0.0052
    ```
    """
    _model = get_model_instance(encoding_name)

    if isinstance(_model, GPTModel):
        num_tokens = num_tokens_from_string(context, encoding_name)
        if _model.pricing.input_price is not None:
            return num_tokens * _model.pricing.input_price
        raise ValueError(f"Model {encoding_name} does not have an input price.")
    else:
        num_tokens = num_tokens_from_string(context, encoding_name)
    raise ValueError(f"{encoding_name} is not a valid GPT model.")


def calc_output(context: str, encoding_name: str) -> float:
    """
    주어진 문맥(context)에서 출력 토큰 개수 기반으로 비용 계산
    
    ```
        >> print(f"${calc_output(lorem, "gpt-4o"):,.2}")
        $0.021
    ```
    """
    _model = get_model_instance(encoding_name)

    if isinstance(_model, GPTModel):
        num_tokens = num_tokens_from_string(context, encoding_name)
        if _model.pricing.output_price is not None:
            return num_tokens * _model.pricing.output_price
        raise ValueError(f"Model {encoding_name} does not have an input price.")
    else:
        num_tokens = num_tokens_from_string(context, encoding_name)
    raise ValueError(f"{encoding_name} is not a valid GPT model.")


def calc_cost(context: str, encoding_name: str) -> float:
    """주어진 문맥(context)에서 임베딩 토큰 개수 기반으로 비용 계산"""
    _model = get_model_instance(encoding_name)

    if isinstance(_model, GPTModel):
        num_tokens = num_tokens_from_string(context, encoding_name)
        if _model.pricing.cost is not None:
            return num_tokens * _model.pricing.cost
        raise ValueError(f"Model {encoding_name} does not have an input price.")
    else:
        num_tokens = num_tokens_from_string(context, encoding_name)
    raise ValueError(f"{encoding_name} is not a valid GPT model.")


__all__ = []