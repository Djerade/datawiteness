from pathlib import Path

from app.domain.claim import RawClaim


class SpreadsheetExtractor:
    """XLSX / CSV via pandas : une cellule numérique = une affirmation, en-têtes = contexte."""

    def extract(self, path: Path, source_id: str) -> list[RawClaim]:
        raise NotImplementedError
