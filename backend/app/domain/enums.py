from enum import Enum


class SourceFormat(str, Enum):
    PDF = "pdf"
    XLSX = "xlsx"
    CSV = "csv"
    HTML = "html"


class SourceStatus(str, Enum):
    UPLOADED = "uploaded"
    EXTRACTING = "extracting"
    EXTRACTED = "extracted"
    FAILED = "failed"


class ExtractionMethod(str, Enum):
    TEXT = "text"          # texte natif du PDF
    TABLE = "table"        # tableau détecté
    OCR = "ocr"            # page scannée
    SPREADSHEET = "spreadsheet"


class ClaimStatus(str, Enum):
    EXTRACTED = "extracted"
    NORMALIZED = "normalized"
    TO_REVIEW = "to_review"    # extraction douteuse (OCR, unité inconnue…)
    VALIDATED = "validated"    # validée par un humain
    REJECTED = "rejected"


class Verdict(str, Enum):
    """Les trois cas de la démonstration + la comparaison invalide."""

    CONCORDANT = "concordant"
    EXPLAINED_DIFFERENCE = "explained_difference"   # période / périmètre / méthode / unité
    UNEXPLAINED_CONTRADICTION = "unexplained_contradiction"
    INVALID_COMPARISON = "invalid_comparison"       # ne désignent pas la même réalité


class DifferenceCause(str, Enum):
    PERIOD = "period"
    GEOGRAPHY = "geography"
    POPULATION = "population"
    DEFINITION = "definition"
    METHOD = "method"
    UNIT = "unit"
    REVISION = "revision"


class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
