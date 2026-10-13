"""Étape 1 — Ingestion : réception d'un fichier, empreinte, stockage, métadonnées."""

import hashlib
from pathlib import Path

from app.domain.enums import SourceFormat

EXTENSIONS = {".pdf": SourceFormat.PDF, ".xlsx": SourceFormat.XLSX, ".csv": SourceFormat.CSV}


def detect_format(filename: str) -> SourceFormat:
    ext = Path(filename).suffix.lower()
    if ext not in EXTENSIONS:
        raise ValueError(f"Format non supporté : {ext}")
    return EXTENSIONS[ext]


def sha256_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def store(data: bytes, filename: str, storage_dir: Path) -> Path:
    """Stocke le fichier sous son empreinte pour éviter les doublons."""
    raise NotImplementedError
