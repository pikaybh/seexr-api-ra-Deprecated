from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from models import BaseRouter



class HomeRouter(BaseRouter):
    def __init__(self):
        super().__init__(prefix="", tags=["Home UI"])
        self.templates = Jinja2Templates(directory="templates")

    def _register_routes(self):
        self.router.add_api_route(
            path="/",
            endpoint=self.read_root,
            methods=["GET"],
            response_class=HTMLResponse,
            description="Home UI for the users who enter the base URL."
        )

    async def read_root(self, request: Request):
        return self.templates.TemplateResponse("index.html", {"request": request})



__all__ = ["HomeRouter"]

