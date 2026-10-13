"""Orchestration du pipeline complet pour un workspace."""


class AnalysisService:
    def ingest(self, workspace_id: str, filename: str, data: bytes) -> str:
        raise NotImplementedError

    def extract(self, source_id: str) -> int:
        raise NotImplementedError

    def run_comparisons(self, workspace_id: str) -> int:
        raise NotImplementedError
