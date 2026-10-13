"""Niveau de confiance expliqué — jamais un score présenté comme une vérité absolue."""

from app.domain.claim import ComparisonResult, ConfidenceAssessment


def assess(result: ComparisonResult) -> ConfidenceAssessment:
    """Combine qualité d'extraction, similarité, complétude des métadonnées, nature de la source."""
    raise NotImplementedError
