from pathlib import Path

from app.domain.claim import RawClaim


class PdfExtractor:
    """Texte natif (PyMuPDF) + tableaux (pdfplumber) + repli OCR (Tesseract) par page."""

    def extract(self, path: Path, source_id: str) -> list[RawClaim]:
        raise NotImplementedError
