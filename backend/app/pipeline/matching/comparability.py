"""Règles explicites : la comparaison est-elle légitime ? (déterministe, testable)."""

from app.domain.claim import Claim, ComparabilityCheck


def check_comparability(a: Claim, b: Claim) -> list[ComparabilityCheck]:
    """Vérifie période, zone, population, unité, définition, méthode."""
    raise NotImplementedError
