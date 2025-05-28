from models import BaseRouter
from schemas import BaseResponse

class HealthRouterV1(BaseRouter):
    def __init__(self):
        super().__init__(prefix="/v1/health", tags=["Health Check"])

    def _register_routes(self):
        self.router.add_api_route(
            path="/",
            endpoint=self.health_check,
            methods=["GET"],
            response_model=BaseResponse,
            description="Health check endpoint to verify if the service is running."
        )

    def health_check(self):
        return BaseResponse(
            status="ok",
            code=200,
            message="Service is running",
            data=None,
            error=None
        )

__all__ = ["HealthRouterV1"]

