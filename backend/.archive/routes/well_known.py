from fastapi import APIRouter


well_known = APIRouter(prefix="/.well-known/acme-challenge")

__all__ = ["well_known"]
