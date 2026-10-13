from fastapi import APIRouter, HTTPException, UploadFile

from app.schemas.source import SourceOut

router = APIRouter()


@router.post("", status_code=201, response_model=SourceOut)
async def upload_source(workspace_id: str, file: UploadFile) -> SourceOut:
    """Dépôt d'un PDF / XLSX / CSV puis lancement de l'extraction en tâche de fond."""
    raise HTTPException(501, "À implémenter")


@router.get("", response_model=list[SourceOut])
def list_sources(workspace_id: str) -> list[SourceOut]:
    raise HTTPException(501, "À implémenter")


@router.get("/{source_id}/file")
def download_source_file(source_id: str):
    """Fichier original, pour afficher la page exacte de la preuve."""
    raise HTTPException(501, "À implémenter")
