"""Étape 5 — Détection : écarts numériques, incohérences, comparaisons non valides."""

from app.domain.claim import Claim, ComparabilityCheck, ComparisonResult
from app.domain.enums import Verdict


def relative_gap(a: float, b: float) -> float:
    denom = max(abs(a), abs(b))
    return 0.0 if denom == 0 else abs(a - b) / denom


def decide_verdict(gap: float, checks: list[ComparabilityCheck], tolerance: float) -> Verdict:
    """Arbre de décision (docs/DOCUMENT_TECHNIQUE.md §7.2)."""
    incompatible = [c for c in checks if not c.compatible]
    if gap <= tolerance:
        return Verdict.CONCORDANT
    if incompatible:
        return Verdict.EXPLAINED_DIFFERENCE
    return Verdict.UNEXPLAINED_CONTRADICTION


def compare(a: Claim, b: Claim, similarity: float, tolerance: float) -> ComparisonResult:
    raise NotImplementedError
