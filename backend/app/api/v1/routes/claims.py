from fastapi import APIRouter, HTTPException

from app.schemas.claim import ClaimOut

router = APIRouter()


@router.get("", response_model=list[ClaimOut])
def list_claims(workspace_id: str, indicator_code: str | None = None) -> list[ClaimOut]:
    raise HTTPException(501, "À implémenter")


@router.patch("/{claim_id}", response_model=ClaimOut)
def review_claim(claim_id: str) -> ClaimOut:
    """Validation / correction humaine d'une valeur extraite (tracée dans audit_event)."""
    raise HTTPException(501, "À implémenter")
