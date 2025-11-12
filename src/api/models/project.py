"""Project database models."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import JSON, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class ProjectType(str, Enum):
    """Project type."""

    NEXTJS = "nextjs"
    FLUTTER = "flutter"
    PYTHON = "python"
    REACT = "react"
    VUE = "vue"
    OTHER = "other"


class Project(Base):
    """Generated project metadata."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Project type and configuration
    project_type: Mapped[str] = mapped_column(String(50), nullable=False)
    template: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    path: Mapped[str] = mapped_column(String(500), nullable=False)  # Local path

    # Metadata
    project_metadata = Column(JSON, nullable=True)  # Additional project metadata
    config = Column(JSON, nullable=True)  # Project configuration used

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Creation details
    created_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    skill_used: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )  # Skill that created it

    # Repository information (optional)
    git_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    git_branch: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        """String representation."""
        return f"<Project(id={self.id}, name={self.name}, type={self.project_type})>"
