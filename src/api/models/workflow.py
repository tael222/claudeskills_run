"""Workflow database models."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import JSON, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class WorkflowStatus(str, Enum):
    """Workflow execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Workflow(Base):
    """Workflow execution record."""

    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=WorkflowStatus.PENDING
    )

    # Execution details
    parameters = Column(JSON, nullable=True)  # Input parameters
    result = Column(JSON, nullable=True)  # Execution result
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Error message

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Metadata
    created_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    tags = Column(JSON, nullable=True)  # Tags for categorization

    def __repr__(self) -> str:
        """String representation."""
        return f"<Workflow(id={self.id}, name={self.name}, status={self.status})>"
