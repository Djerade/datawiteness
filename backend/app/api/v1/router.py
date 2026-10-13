from fastapi import APIRouter

from app.api.v1.routes import claims, comparisons, graph, health, sources, workspaces

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["workspaces"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(claims.router, prefix="/claims", tags=["claims"])
api_router.include_router(comparisons.router, prefix="/comparisons", tags=["comparisons"])
api_router.include_router(graph.router, prefix="/graph", tags=["graph"])
