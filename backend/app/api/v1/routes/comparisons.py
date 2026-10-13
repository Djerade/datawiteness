from fastapi import APIRouter, HTTPException

from app.domain.enums import Verdict
from app.schemas.comparison import ComparisonOut, EvidenceCardOut

router = APIRouter()


@router.post("/run", status_code=202)
def run_comparisons(workspace_id: str) -> dict:
    raise HTTPException(501, "À implémenter")


@router.get("", response_model=list[ComparisonOut])
def list_comparisons(workspace_id: str, verdict: Verdict | None = None) -> list[ComparisonOut]:
    raise HTTPException(501, "À implémenter")


@router.get("/{comparison_id}/evidence", response_model=EvidenceCardOut)
def evidence_card(comparison_id: str) -> EvidenceCardOut:
    raise HTTPException(501, "À implémenter")
