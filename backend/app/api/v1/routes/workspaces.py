from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("", status_code=201)
def create_workspace() -> dict:
    raise HTTPException(501, "À implémenter")


@router.get("")
def list_workspaces() -> list[dict]:
    raise HTTPException(501, "À implémenter")
