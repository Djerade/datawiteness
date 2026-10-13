"""Objets métier purs (sans dépendance à la base), manipulés par le pipeline."""

from dataclasses import dataclass, field

from app.domain.enums import ConfidenceLevel, DifferenceCause, ExtractionMethod, Verdict


@dataclass(frozen=True)
class EvidenceLocation:
    source_id: str
    page: int | None
    table_ref: str | None
    snippet: str
    bbox: tuple[float, float, float, float] | None = None


@dataclass
class RawClaim:
    """Affirmation quantitative telle qu'extraite, avant normalisation."""

    indicator_label: str
    value_text: str
    unit_text: str | None
    period_text: str | None
    zone_text: str | None
    population_text: str | None
    context: str
    location: EvidenceLocation
    method: ExtractionMethod
    extraction_confidence: float


@dataclass
class Claim:
    """Affirmation normalisée, comparable."""

    id: str
    indicator_code: str | None
    value: float
    unit: str
    period_start: str | None
    period_end: str | None
    zone_code: str | None
    population: str | None
    definition: str | None
    location: EvidenceLocation
    extraction_confidence: float


@dataclass
class ComparabilityCheck:
    dimension: DifferenceCause
    compatible: bool
    detail: str


@dataclass
class ComparisonResult:
    claim_a: Claim
    claim_b: Claim
    similarity: float
    checks: list[ComparabilityCheck]
    relative_gap: float | None
    verdict: Verdict
    causes: list[DifferenceCause] = field(default_factory=list)


@dataclass
class ConfidenceAssessment:
    level: ConfidenceLevel
    score: float
    reasons: list[str]
