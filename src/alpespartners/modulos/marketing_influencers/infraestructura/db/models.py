import uuid
from datetime import datetime

from sqlalchemy import (
    String, Integer, DateTime, func, text, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Campaña(Base):
    __tablename__ = "campaigns"

    id: Mapped[uuid.UUID]                  = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str]                    = mapped_column(String(200), nullable=False)
    estado: Mapped[str]                    = mapped_column(String(40), default="CREATED", nullable=False)
    version: Mapped[int]                   = mapped_column(Integer, default=1, nullable=False)
    creacion_comando_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True)
    creado_en: Mapped[datetime]           = mapped_column(DateTime(timezone=True), server_default=func.now())

class Outbox(Base):
    __tablename__ = "outbox"
    __table_args__ = (UniqueConstraint("command_id", name="uq_outbox_command"), )

    id: Mapped[uuid.UUID]           = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aggregate_type: Mapped[str]     = mapped_column(String(80), nullable=False)
    aggregate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    type: Mapped[str]               = mapped_column(String(120), nullable=False)
    payload: Mapped[dict]           = mapped_column(JSONB, nullable=False)
    headers: Mapped[dict]           = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    status: Mapped[str]             = mapped_column(String(20), nullable=False, default="PENDING", index=True)
    command_id: Mapped[uuid.UUID]   = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime]    = mapped_column(DateTime(timezone=True), server_default=func.now())
    sent_at: Mapped[datetime]       = mapped_column(DateTime(timezone=True), nullable=True)
