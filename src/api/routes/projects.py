"""Projects API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import Project, ProjectCreate, ProjectListResponse, ProjectResponse
from src.core.database import get_async_db
from src.core.logger import logger

router = APIRouter()


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
) -> ProjectListResponse:
    """List all projects."""
    try:
        query = select(Project).offset(skip).limit(limit).order_by(Project.created_at.desc())

        result = await db.execute(query)
        projects = result.scalars().all()

        count_result = await db.execute(select(Project))
        total = len(count_result.scalars().all())

        return ProjectListResponse(
            projects=[ProjectResponse.model_validate(p) for p in projects], total=total
        )
    except Exception as e:
        logger.error(f"Failed to list projects: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list projects: {str(e)}",
        )


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_async_db),
) -> ProjectResponse:
    """Create a new project."""
    try:
        project = Project(
            name=project_data.name,
            display_name=project_data.display_name,
            description=project_data.description,
            project_type=project_data.project_type,
            template=project_data.template,
            path=project_data.path,
            config=project_data.config,
            project_metadata=project_data.project_metadata,
        )

        db.add(project)
        await db.commit()
        await db.refresh(project)

        logger.info(f"Created project: {project.name} (ID: {project.id})")
        return ProjectResponse.model_validate(project)
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to create project: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create project: {str(e)}",
        )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> ProjectResponse:
    """Get project by ID."""
    try:
        result = await db.execute(select(Project).where(Project.id == project_id))
        project = result.scalar_one_or_none()

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found",
            )

        return ProjectResponse.model_validate(project)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get project: {str(e)}",
        )
