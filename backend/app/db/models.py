"""Modèle de données persistant (voir docs/DOCUMENT_TECHNIQUE.md §6)."""

import uuid
from datetime import date, datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.domain.enums import (
    ClaimStatus,
    ConfidenceLevel,
    ExtractionMethod,
    SourceFormat,
    SourceStatus,
    Verdict,
)

EMBEDDING_DIM = 384


def _uuid() -> str:
    return str(uuid.uuid4())


class Workspace(Base):
    """Un dossier d'analyse (ex. « Éducation Togo 2020-2024 »)."""

    __tablename__ = "workspace"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(200))
    domain: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    sources: Mapped[list["Source"]] = relationship(back_populates="workspace")


class Source(Base):
    __tablename__ = "source"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspace.id"))
    title: Mapped[str] = mapped_column(String(500))
    publisher: Mapped[str | None] = mapped_column(String(200))
    published_on: Mapped[date | None] = mapped_column(Date)
    url: Mapped[str | None] = mapped_column(Text)
    license: Mapped[str | None] = mapped_column(String(200))
    format: Mapped[SourceFormat] = mapped_column(Enum(SourceFormat))
    file_path: Mapped[str] = mapped_column(Text)
    sha256: Mapped[str] = mapped_column(String(64), unique=True)
    status: Mapped[SourceStatus] = mapped_column(Enum(SourceStatus), default=SourceStatus.UPLOADED)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    workspace: Mapped[Workspace] = relationship(back_populates="sources")
    fragments: Mapped[list["Fragment"]] = relationship(back_populates="source")


class Fragment(Base):
    """Passage localisé d'une source : la preuve physique."""

    __tablename__ = "fragment"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    source_id: Mapped[str] = mapped_column(ForeignKey("source.id"))
    page: Mapped[int | None] = mapped_column(Integer)
    table_ref: Mapped[str | None] = mapped_column(String(100))
    bbox: Mapped[list | None] = mapped_column(JSON)
    text: Mapped[str] = mapped_column(Text)
    method: Mapped[ExtractionMethod] = mapped_column(Enum(ExtractionMethod))
    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBEDDING_DIM))
    source: Mapped[Source] = relationship(back_populates="fragments")


class Indicator(Base):
    """Indicateur canonique du référentiel (data/referentiels/indicateurs.yaml)."""

    __tablename__ = "indicator"
    code: Mapped[str] = mapped_column(String(50), primary_key=True)
    label: Mapped[str] = mapped_column(String(300))
    synonyms: Mapped[list] = mapped_column(JSON, default=list)
    definition: Mapped[str | None] = mapped_column(Text)
    unit: Mapped[str | None] = mapped_column(String(30))
    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBEDDING_DIM))


class Claim(Base):
    """Affirmation quantitative extraite et normalisée."""

    __tablename__ = "claim"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    fragment_id: Mapped[str] = mapped_column(ForeignKey("fragment.id"))
    indicator_code: Mapped[str | None] = mapped_column(ForeignKey("indicator.code"))
    indicator_label_raw: Mapped[str] = mapped_column(String(500))
    value: Mapped[float] = mapped_column(Float)
    value_raw: Mapped[str] = mapped_column(String(100))
    unit: Mapped[str | None] = mapped_column(String(30))
    period_start: Mapped[date | None] = mapped_column(Date)
    period_end: Mapped[date | None] = mapped_column(Date)
    zone_code: Mapped[str | None] = mapped_column(String(30))
    population: Mapped[str | None] = mapped_column(String(200))
    definition: Mapped[str | None] = mapped_column(Text)
    method_note: Mapped[str | None] = mapped_column(Text)
    extraction_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[ClaimStatus] = mapped_column(Enum(ClaimStatus), default=ClaimStatus.EXTRACTED)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBEDDING_DIM))
    fragment: Mapped[Fragment] = relationship()


class Comparison(Base):
    """Rapprochement de deux affirmations et verdict."""

    __tablename__ = "comparison"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    claim_a_id: Mapped[str] = mapped_column(ForeignKey("claim.id"))
    claim_b_id: Mapped[str] = mapped_column(ForeignKey("claim.id"))
    similarity: Mapped[float] = mapped_column(Float)
    relative_gap: Mapped[float | None] = mapped_column(Float)
    checks: Mapped[list] = mapped_column(JSON, default=list)
    causes: Mapped[list] = mapped_column(JSON, default=list)
    verdict: Mapped[Verdict] = mapped_column(Enum(Verdict))
    confidence_level: Mapped[ConfidenceLevel] = mapped_column(Enum(ConfidenceLevel))
    confidence_score: Mapped[float] = mapped_column(Float)
    confidence_reasons: Mapped[list] = mapped_column(JSON, default=list)
    explanation: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    claim_a: Mapped[Claim] = relationship(foreign_keys=[claim_a_id])
    claim_b: Mapped[Claim] = relationship(foreign_keys=[claim_b_id])


class AuditEvent(Base):
    """Journal de vérification : chaque étape du pipeline et chaque action humaine."""

    __tablename__ = "audit_event"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    entity_type: Mapped[str] = mapped_column(String(50))
    entity_id: Mapped[str] = mapped_column(String(36))
    action: Mapped[str] = mapped_column(String(100))
    actor: Mapped[str] = mapped_column(String(100), default="system")
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
