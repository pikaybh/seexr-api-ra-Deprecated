from typing import List, Literal

from fastapi import Query, HTTPException

from models import BaseRouter
from schemas import Provider, LargeLanguageModel

language_models = [
    Provider(
        name="OpenAI",
        alias="openai",
        models=[
            LargeLanguageModel(name="gpt-4", type="chat", available=True),
            LargeLanguageModel(name="gpt-4o-mini", type="chat", available=True),
            LargeLanguageModel(name="text-embedding-ada-002", type="embedding", available=True),
        ]
    ),
    Provider(
        name="DeepSeek",
        alias="ds",
        models=[
            LargeLanguageModel(name="deepseek-r1:32b", type="chat", available=False),
        ]
    ),
    Provider(
        name="LG AI",
        alias="lgai",
        models=[
            LargeLanguageModel(name="exaone3.5:latest", type="chat", available=False),
        ]
    )
]

class ModelListRouter(BaseRouter):
    def __init__(self):
        super().__init__(prefix="/v1/list", tags=["List of Models"])

    def _register_routes(self):
        self.router.add_api_route(
            path="/models",
            endpoint=self.get_all_models,
            methods=["GET"],
            response_model=List[Provider],
            description="모든 언어 모델 목록을 조회하거나, 사용 가능한 모델만 필터링합니다."
        )
        self.router.add_api_route(
            path="/models/{provider}",
            endpoint=self.get_models,
            methods=["GET"],
            response_model=Provider,
            description="특정 제공자의 모델 목록을 조회하거나, 사용 가능한 모델만 필터링합니다."
        )

    def get_all_models(
            self,
            filter: Literal["all", "available"] = Query("available", description="Filter type: 'all' or 'available'"),
        ) -> List[Provider]:
        if filter == "all":
            return language_models
        elif filter == "available":
            return [
                Provider(
                    name=lm.name,
                    alias=lm.alias,
                    models=[model for model in lm.models if model.available]
                ) for lm in language_models
            ]
        else:
            raise HTTPException(400, detail="Invalid filter type. Use 'all' or 'available'.")

    def get_models(
            self,
            provider: str,
            filter: Literal["all", "available"] = Query("available", description="Filter type: 'all' or 'available'"),
        ) -> Provider:
        lm = next((lm for lm in language_models if lm.name.lower() == provider.lower() or lm.alias.lower() == provider.lower()), None)
        if not lm:
            raise HTTPException(404, f"Provider '{provider}' not found.")
        if filter == "all":
            return lm
        elif filter == "available":
            return Provider(
                name=lm.name,
                alias=lm.alias,
                models=[model for model in lm.models if model.available]
            )
        else:
            raise HTTPException(400, detail="Invalid filter type. Use 'all' or 'available'.")

__all__ = ["ModelListRouter"]

