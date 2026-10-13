"""Étape 2 — Extraction : texte, tableaux, valeurs, unités, dates et métadonnées."""

from pathlib import Path
from typing import Protocol

from app.domain.claim import RawClaim


class Extractor(Protocol):
    def extract(self, path: Path, source_id: str) -> list[RawClaim]: ...
