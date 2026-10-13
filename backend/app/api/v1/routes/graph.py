from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("")
def provenance_graph(workspace_id: str, indicator_code: str | None = None) -> dict:
    """Nœuds (indicateur, valeur, source, période, territoire) et arêtes, format Cytoscape."""
    raise HTTPException(501, "À implémenter")
