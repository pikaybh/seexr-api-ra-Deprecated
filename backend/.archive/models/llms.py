"""
TODO: Archive this file.
"""

from schemas import LargeLanguageModel, Provider

__all__ = []

class LLMs:
    """
    Represents a collection of large language models (LLMs) and their providers.
    """
    def __init__(self, providers=[]):
        self.providers = providers

    def add_provider(self, provider: Provider):
        """
        Adds a new provider to the collection.
        """
        self.providers.append(provider)

    def get_providers(self):
        """
        Returns the list of providers.
        """
        return self.providers
    
    def add_model(self, model: LargeLanguageModel, provider_name: str):
        """
        Adds a new model to the specified provider.
        """
        for provider in self.providers:
            if provider.name == provider_name:
                provider.models.append(model)
                return
        raise ValueError(f"Provider '{provider_name}' not found.")
    
    def _get_all_models(self):
        """
        Returns a flat list of all models from all providers.
        """
        return [model for provider in self.providers for model in provider.models]
    
    def _get_available_models(self):
        """
        Returns a flat list of all available models from all providers.
        """
        return [model for provider in self.providers for model in provider.models if model.available]

    def get_models(self, **kwargs):
        """
        Returns a flat list of all models from all providers.
        """
        if kwargs.get("all", False):
            return self._get_all_models()
        elif kwargs.get("available", False):
            return self._get_available_models()
    


ra_language_models = LLMs(
    providers=[
        Provider(
            name="DeepSeek",
            alias="ds",
            models=[
                LargeLanguageModel(name="llama3.1", type="chat", available=True),
                LargeLanguageModel(name="llama3.2", type="chat", available=True),
                LargeLanguageModel(name="llama3.3", type="chat", available=True),
                LargeLanguageModel(name="llama3.4", type="chat", available=True),
                LargeLanguageModel(name="mistral-7b-instruct-v0.1", type="chat", available=True),
                LargeLanguageModel(name="mistral-7b-instruct-v0.2", type="chat", available=True),
                LargeLanguageModel(name="mistral-7b-instruct-v0.3", type="chat", available=True),
            ]
        ),
        Provider(
            name="OpenAI",
            models=[
                LargeLanguageModel(name="gpt-4o-mini", type="chat", available=True),
                LargeLanguageModel(name="gpt-4o", type="chat", available=True),
            ]
        ),
    ]
)
