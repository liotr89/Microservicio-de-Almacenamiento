from fastapi import APIRouter, HTTPException, status
from typing import Optional

from app.models import EvidenceCreate, EvidenceResponse
from app.services.storage import storage_service

router = APIRouter(prefix="/api/evidence", tags=["evidence"])


@router.post("", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED)
def create_evidence(evidence: EvidenceCreate):
    try:
        evidence_id = storage_service.store(evidence.contenido)

        stored = storage_service.retrieve(evidence_id)
        if not stored:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve stored evidence",
            )

        return EvidenceResponse(**stored)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store evidence: {str(e)}",
        )


@router.get("/{evidence_id}", response_model=EvidenceResponse)
def get_evidence(evidence_id: str):
    stored = storage_service.retrieve(evidence_id)

    if not stored:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence {evidence_id} not found",
        )

    return EvidenceResponse(**stored)
