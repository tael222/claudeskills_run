"""Workflow API endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import (
    Workflow,
    WorkflowCreate,
    WorkflowListResponse,
    WorkflowResponse,
    WorkflowStatus,
    WorkflowUpdate,
)
from src.core.database import get_async_db
from src.core.logger import logger

router = APIRouter()


@router.get("", response_model=WorkflowListResponse)
async def list_workflows(
    skip: int = 0,
    limit: int = 100,
    status_filter: WorkflowStatus | None = None,
    db: AsyncSession = Depends(get_async_db),
) -> WorkflowListResponse:
    """
    List all workflows with optional filtering.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status_filter: Filter by workflow status
        db: Database session

    Returns:
        List of workflows with total count
    """
    try:
        query = select(Workflow)

        if status_filter:
            query = query.where(Workflow.status == status_filter)

        query = query.offset(skip).limit(limit).order_by(Workflow.created_at.desc())

        result = await db.execute(query)
        workflows = result.scalars().all()

        # Get total count
        count_query = select(Workflow)
        if status_filter:
            count_query = count_query.where(Workflow.status == status_filter)

        count_result = await db.execute(count_query)
        total = len(count_result.scalars().all())

        return WorkflowListResponse(
            workflows=[WorkflowResponse.model_validate(w) for w in workflows], total=total
        )
    except Exception as e:
        logger.error(f"Failed to list workflows: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list workflows: {str(e)}",
        )


@router.post("", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    workflow_data: WorkflowCreate,
    db: AsyncSession = Depends(get_async_db),
) -> WorkflowResponse:
    """
    Create a new workflow.

    Args:
        workflow_data: Workflow creation data
        db: Database session

    Returns:
        Created workflow
    """
    try:
        workflow = Workflow(
            name=workflow_data.name,
            description=workflow_data.description,
            parameters=workflow_data.parameters,
            tags=workflow_data.tags,
            status=WorkflowStatus.PENDING,
        )

        db.add(workflow)
        await db.commit()
        await db.refresh(workflow)

        logger.info(f"Created workflow: {workflow.name} (ID: {workflow.id})")
        return WorkflowResponse.model_validate(workflow)
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to create workflow: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create workflow: {str(e)}",
        )


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> WorkflowResponse:
    """
    Get workflow by ID.

    Args:
        workflow_id: Workflow ID
        db: Database session

    Returns:
        Workflow details
    """
    try:
        result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
        workflow = result.scalar_one_or_none()

        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow {workflow_id} not found",
            )

        return WorkflowResponse.model_validate(workflow)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get workflow {workflow_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get workflow: {str(e)}",
        )


@router.patch("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: int,
    workflow_data: WorkflowUpdate,
    db: AsyncSession = Depends(get_async_db),
) -> WorkflowResponse:
    """
    Update workflow.

    Args:
        workflow_id: Workflow ID
        workflow_data: Workflow update data
        db: Database session

    Returns:
        Updated workflow
    """
    try:
        result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
        workflow = result.scalar_one_or_none()

        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow {workflow_id} not found",
            )

        # Update fields
        update_data = workflow_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(workflow, field, value)

        await db.commit()
        await db.refresh(workflow)

        logger.info(f"Updated workflow: {workflow.name} (ID: {workflow.id})")
        return WorkflowResponse.model_validate(workflow)
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to update workflow {workflow_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update workflow: {str(e)}",
        )


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(
    workflow_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> None:
    """
    Delete workflow.

    Args:
        workflow_id: Workflow ID
        db: Database session
    """
    try:
        result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
        workflow = result.scalar_one_or_none()

        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow {workflow_id} not found",
            )

        await db.delete(workflow)
        await db.commit()

        logger.info(f"Deleted workflow: {workflow.name} (ID: {workflow.id})")
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to delete workflow {workflow_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete workflow: {str(e)}",
        )
