"""Base workflow engine."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import Workflow, WorkflowStatus
from src.core.logger import logger


class BaseWorkflow(ABC):
    """Base class for all workflows."""

    def __init__(self, db: AsyncSession, workflow_id: int):
        """
        Initialize workflow.

        Args:
            db: Database session
            workflow_id: Workflow database ID
        """
        self.db = db
        self.workflow_id = workflow_id
        self.workflow: Optional[Workflow] = None

    async def load_workflow(self) -> Workflow:
        """Load workflow from database."""
        from sqlalchemy import select

        result = await self.db.execute(select(Workflow).where(Workflow.id == self.workflow_id))
        workflow = result.scalar_one_or_none()

        if not workflow:
            raise ValueError(f"Workflow {self.workflow_id} not found")

        self.workflow = workflow
        return workflow

    async def update_status(
        self,
        status: WorkflowStatus,
        error: Optional[str] = None,
        result: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Update workflow status.

        Args:
            status: New status
            error: Error message if failed
            result: Result data if completed
        """
        if not self.workflow:
            await self.load_workflow()

        self.workflow.status = status

        if status == WorkflowStatus.RUNNING and not self.workflow.started_at:
            self.workflow.started_at = datetime.utcnow()

        if status in (WorkflowStatus.COMPLETED, WorkflowStatus.FAILED):
            self.workflow.completed_at = datetime.utcnow()

        if error:
            self.workflow.error = error

        if result:
            self.workflow.result = result

        await self.db.commit()
        await self.db.refresh(self.workflow)

    async def execute(self) -> dict[str, Any]:
        """
        Execute workflow with error handling.

        Returns:
            Workflow execution result
        """
        try:
            # Load workflow
            await self.load_workflow()
            logger.info(f"Starting workflow {self.workflow.name} (ID: {self.workflow_id})")

            # Update status to running
            await self.update_status(WorkflowStatus.RUNNING)

            # Execute workflow logic
            result = await self.run()

            # Update status to completed
            await self.update_status(WorkflowStatus.COMPLETED, result=result)

            logger.info(
                f"Workflow {self.workflow.name} (ID: {self.workflow_id}) completed successfully"
            )
            return result

        except Exception as e:
            logger.error(f"Workflow {self.workflow_id} failed: {e}")
            await self.update_status(WorkflowStatus.FAILED, error=str(e))
            raise

    @abstractmethod
    async def run(self) -> dict[str, Any]:
        """
        Execute workflow logic.

        This method must be implemented by subclasses.

        Returns:
            Workflow execution result
        """
        pass
