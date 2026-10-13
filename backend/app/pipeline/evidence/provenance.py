"""Étape 7 — Preuve : liens, pages, extraits, provenance et journal de vérification."""

from app.domain.claim import ComparisonResult


def build_evidence_card(result: ComparisonResult) -> dict:
    """Fiche de résultat : deux valeurs, contextes, passages sources, verdict, confiance."""
    raise NotImplementedError
