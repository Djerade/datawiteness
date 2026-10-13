"""Étape 4 — Rapprochement : recherche sémantique + règles explicites de comparabilité."""

from app.domain.claim import Claim


class SemanticMatcher:
    """Embeddings multilingues (pgvector) + similarité floue sur les libellés."""

    def candidates(
        self, claim: Claim, pool: list[Claim], top_k: int = 10
    ) -> list[tuple[Claim, float]]:
        raise NotImplementedError
