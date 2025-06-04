import yaml

def load_allowed_origins(raw: bool = False) -> list | dict:
    """
    allowed_origins.yaml 파일에서 허용된 origin 리스트를 불러옵니다.
    - raw=True: yaml 파싱 결과(list of dict)를 그대로 반환
    - raw=False: 모든 origin을 평탄화(flatten)하여 리스트로 반환
    """
    with open('allowed_origins.yaml', 'r') as f:
        allowed_origins = yaml.safe_load(f)

    if raw:
        return allowed_origins

    handled_origins = []
    for corp in allowed_origins.values():
        for origin in corp.values():
            handled_origins.append(origin)
    return handled_origins

__all__ = [
    "load_allowed_origins",
]