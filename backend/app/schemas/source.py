from datetime import date, datetime

from app.domain.enums import SourceFormat, SourceStatus
from app.schemas.common import ORMModel


class SourceOut(ORMModel):
    id: str
    workspace_id: str
    title: str
    publisher: str | None
    published_on: date | None
    url: str | None
    format: SourceFormat
    status: SourceStatus
    created_at: datetime
