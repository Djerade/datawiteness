from datetime import date

from app.domain.enums import ClaimStatus
from app.schemas.common import ORMModel


class EvidenceOut(ORMModel):
    source_id: str
    source_title: str
    page: int | None
    table_ref: str | None
    snippet: str


class ClaimOut(ORMModel):
    id: str
    indicator_code: str | None
    indicator_label_raw: str
    value: float
    unit: str | None
    period_start: date | None
    period_end: date | None
    zone_code: str | None
    population: str | None
    status: ClaimStatus
    extraction_confidence: float
