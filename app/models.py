from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EvidenceCreate(BaseModel):
    contenido: str = Field(..., description="Contenido de la evidencia (texto o JSON)")


class EvidenceResponse(BaseModel):
    id: str = Field(..., description="ID único de la evidencia")
    contenido: str = Field(..., description="Contenido almacenado")
    created_at: Optional[str] = None
    content_type: str = "text/plain"


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
