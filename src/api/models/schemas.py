"""Pydantic schemas for API requests and responses."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from src.api.models.project import ProjectType
from src.api.models.workflow import WorkflowStatus


# Workflow Schemas
class WorkflowBase(BaseModel):
    """Base workflow schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    parameters: Optional[dict[str, Any]] = None
    tags: Optional[list[str]] = None


class WorkflowCreate(WorkflowBase):
    """Create workflow request."""

    pass


class WorkflowUpdate(BaseModel):
    """Update workflow request."""

    description: Optional[str] = None
    status: Optional[WorkflowStatus] = None
    result: Optional[dict[str, Any]] = None
    error: Optional[str] = None


class WorkflowResponse(WorkflowBase):
    """Workflow response."""

    id: int
    status: WorkflowStatus
    result: Optional[dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_by: Optional[str] = None

    model_config = {"from_attributes": True}


# Skill Schemas
class SkillBase(BaseModel):
    """Base skill schema."""

    name: str = Field(..., min_length=1, max_length=255)
    display_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    version: str = Field(default="0.1.0", pattern=r"^\d+\.\d+\.\d+$")
    config: Optional[dict[str, Any]] = None


class SkillCreate(SkillBase):
    """Create skill request."""

    source_path: Optional[str] = None
    source_url: Optional[str] = None
    prompts: Optional[dict[str, str]] = None
    examples: Optional[list[dict[str, Any]]] = None


class SkillUpdate(BaseModel):
    """Update skill request."""

    display_name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    config: Optional[dict[str, Any]] = None
    enabled: Optional[bool] = None


class SkillResponse(SkillBase):
    """Skill response."""

    id: int
    enabled: bool
    is_builtin: bool
    source_path: Optional[str] = None
    source_url: Optional[str] = None
    usage_count: int
    last_used_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Project Schemas
class ProjectBase(BaseModel):
    """Base project schema."""

    name: str = Field(..., min_length=1, max_length=255)
    display_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    project_type: ProjectType
    template: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Create project request."""

    path: str = Field(..., min_length=1, max_length=500)
    config: Optional[dict[str, Any]] = None
    project_metadata: Optional[dict[str, Any]] = None


class ProjectUpdate(BaseModel):
    """Update project request."""

    display_name: Optional[str] = None
    description: Optional[str] = None
    project_metadata: Optional[dict[str, Any]] = None
    git_url: Optional[str] = None
    git_branch: Optional[str] = None


class ProjectResponse(ProjectBase):
    """Project response."""

    id: int
    path: str
    project_metadata: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    skill_used: Optional[str] = None
    git_url: Optional[str] = None
    git_branch: Optional[str] = None

    model_config = {"from_attributes": True}


# List responses
class WorkflowListResponse(BaseModel):
    """List of workflows."""

    workflows: list[WorkflowResponse]
    total: int


class SkillListResponse(BaseModel):
    """List of skills."""

    skills: list[SkillResponse]
    total: int


class ProjectListResponse(BaseModel):
    """List of projects."""

    projects: list[ProjectResponse]
    total: int
