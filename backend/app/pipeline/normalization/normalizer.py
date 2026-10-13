"""Étape 3 — Normalisation : indicateurs, périodes, zones, unités, définitions."""

from app.domain.claim import Claim, RawClaim


class Normalizer:
    """S'appuie sur data/referentiels/*.yaml. Une valeur non normalisable passe en TO_REVIEW."""

    def normalize(self, raw: RawClaim) -> Claim:
        raise NotImplementedError

    def normalize_period(self, text: str | None) -> tuple[str | None, str | None]:
        """« 2019-2020 », « année scolaire 2019/2020 », « 2021 » → (début, fin) ISO."""
        raise NotImplementedError

    def normalize_unit(self, text: str | None) -> tuple[str | None, float]:
        """Retourne (code unité canonique, facteur de conversion)."""
        raise NotImplementedError

    def normalize_zone(self, text: str | None) -> str | None:
        raise NotImplementedError
