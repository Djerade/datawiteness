from app.domain.enums import ConfidenceLevel, Verdict
from app.schemas.claim import ClaimOut, EvidenceOut
from app.schemas.common import ORMModel


class ComparisonOut(ORMModel):
    id: str
    claim_a: ClaimOut
    claim_b: ClaimOut
    similarity: float
    relative_gap: float | None
    checks: list[dict]
    causes: list[str]
    verdict: Verdict
    confidence_level: ConfidenceLevel
    confidence_score: float
    confidence_reasons: list[str]
    explanation: str | None


class EvidenceCardOut(ORMModel):
    comparison: ComparisonOut
    evidence_a: EvidenceOut
    evidence_b: EvidenceOut
